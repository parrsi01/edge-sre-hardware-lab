#include <arpa/inet.h>
#include <atomic>
#include <chrono>
#include <csignal>
#include <cstring>
#include <iomanip>
#include <iostream>
#include <netinet/in.h>
#include <sstream>
#include <string>
#include <sys/socket.h>
#include <thread>
#include <unistd.h>

namespace {
std::atomic<bool> running{true};
std::atomic<bool> fault_enabled{false};
std::atomic<unsigned long> sequence{0};
const auto started_at = std::chrono::steady_clock::now();

void stop_server(int) { running = false; }

std::string reading_json() {
    const auto seq = ++sequence;
    const auto uptime = std::chrono::duration_cast<std::chrono::seconds>(
        std::chrono::steady_clock::now() - started_at).count();
    if (fault_enabled) {
        return R"({"status":"fault","error":"simulated_device_fault"})";
    }
    const double temperature = 39.0 + static_cast<double>(seq % 8) * 0.35;
    const double voltage = 12.0 + static_cast<double>(seq % 3) * 0.01;
    std::ostringstream output;
    output << std::fixed << std::setprecision(2)
           << R"({"device_id":"edge-node-01","sequence":)" << seq
           << R"(,"temperature_c":)" << temperature
           << R"(,"voltage_v":)" << voltage
           << R"(,"uptime_seconds":)" << uptime
           << R"(,"status":"ok"})";
    return output.str();
}

std::string handle_command(const std::string& input) {
    if (input == "READ") return reading_json();
    if (input == "PING") return R"({"status":"ok","reply":"PONG"})";
    if (input == "SET_FAIL ON") {
        fault_enabled = true;
        return R"({"status":"ok","fault_enabled":true})";
    }
    if (input == "SET_FAIL OFF") {
        fault_enabled = false;
        return R"({"status":"ok","fault_enabled":false})";
    }
    return R"({"status":"error","error":"unknown_command"})";
}

bool self_test() {
    fault_enabled = false;
    const auto healthy = handle_command("READ");
    if (healthy.find("edge-node-01") == std::string::npos) return false;
    handle_command("SET_FAIL ON");
    const auto failed = handle_command("READ");
    handle_command("SET_FAIL OFF");
    return failed.find("simulated_device_fault") != std::string::npos &&
           handle_command("NOPE").find("unknown_command") != std::string::npos;
}

void serve_client(int client) {
    char buffer[1024]{};
    const auto received = read(client, buffer, sizeof(buffer) - 1);
    if (received <= 0) {
        close(client);
        return;
    }
    std::string input(buffer, static_cast<std::size_t>(received));
    while (!input.empty() && (input.back() == '\n' || input.back() == '\r')) input.pop_back();
    const std::string response = handle_command(input) + "\n";
    send(client, response.data(), response.size(), 0);
    close(client);
}
}  // namespace

int main(int argc, char** argv) {
    if (argc == 2 && std::string(argv[1]) == "--self-test") {
        if (!self_test()) return 1;
        std::cout << "self-test passed\n";
        return 0;
    }

    std::signal(SIGINT, stop_server);
    std::signal(SIGTERM, stop_server);
    const int server = socket(AF_INET, SOCK_STREAM, 0);
    if (server < 0) {
        std::cerr << "socket creation failed\n";
        return 1;
    }
    int reuse = 1;
    setsockopt(server, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));
    sockaddr_in address{};
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(9101);
    if (bind(server, reinterpret_cast<sockaddr*>(&address), sizeof(address)) < 0 || listen(server, 16) < 0) {
        std::cerr << "bind/listen failed: " << std::strerror(errno) << "\n";
        close(server);
        return 1;
    }
    std::cout << "device simulator listening on 9101\n";
    while (running) {
        const int client = accept(server, nullptr, nullptr);
        if (client < 0) {
            if (running) std::cerr << "accept failed\n";
            continue;
        }
        std::thread(serve_client, client).detach();
    }
    close(server);
    return 0;
}
