FROM gcc:14-bookworm AS builder
RUN apt-get update && apt-get install -y --no-install-recommends cmake && rm -rf /var/lib/apt/lists/*
WORKDIR /src
COPY CMakeLists.txt .
COPY src ./src
RUN cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build --parallel

FROM gcc:14-bookworm
RUN useradd --system --uid 10001 --create-home appuser
WORKDIR /app
COPY --from=builder /src/build/device-simulator /app/device-simulator
USER appuser
EXPOSE 9101
ENTRYPOINT ["/app/device-simulator"]
