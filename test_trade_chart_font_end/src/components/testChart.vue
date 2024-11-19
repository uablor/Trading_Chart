<!-- <template>
  <div class="chart-container">
    <div class="toolbar">
      <button @click="setTimeRange('1D')">1D</button>
      <button @click="setTimeRange('1W')">1W</button>
      <button @click="setTimeRange('1M')">1M</button>
      <button @click="toggleLiveData">{{ liveData ? 'Pause' : 'Resume' }} Live Data</button>
    </div>
    <apexchart 
      ref="chart"
      type="candlestick" 
      :options="chartOptions" 
      :series="series" 
      class="chart"
    ></apexchart>
  </div>
</template>

<script>
import ApexCharts from 'vue3-apexcharts';

export default {
  components: { ApexCharts },
  data() {
    return {
      series: [
        {
          data: [] // This will hold the initial and live data
        }
      ],
      chartOptions: {
        chart: {
          type: 'candlestick',
          height: 600,
          width: '100%',
          animations: {
            enabled: true,
            easing: 'easeinout',
            speed: 800
          },
          toolbar: {
            show: true,
            tools: {
              download: true,
              zoom: true,
              zoomin: true,
              zoomout: true,
              pan: true,
              reset: true
            }
          },
          background: '#f4f4f8',
          foreColor: '#333',
        },
        xaxis: {
          type: 'datetime'
        },
        yaxis: {
          tooltip: { enabled: true }
        },
        tooltip: {
          enabled: true,
          theme: 'dark'
        },
      },
      liveData: true // Control for enabling/disabling live data
    };
  },
  mounted() {
    this.fetchInitialData();
    this.connectWebSocket();
  },
  methods: {
    async fetchInitialData() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/klines/');
        const data = await response.json();
        this.series[0].data = data.map(d => ({
          x: new Date(d.time * 1000),
          y: [d.open, d.high, d.low, d.close]
        }));
      } catch (error) {
        console.error("Error fetching initial data:", error);
      }
    },
    connectWebSocket() {
      const socket = new WebSocket('ws://127.0.0.1:9000/ws/klines/');
      socket.onmessage = (event) => {
        if (!this.liveData) return; // Stop updates if liveData is paused
        const newPoint = JSON.parse(event.data);
        const updatedData = {
          x: new Date(newPoint.time * 1000),
          y: [newPoint.open, newPoint.high, newPoint.low, newPoint.close]
        };
        this.series[0].data.push(updatedData);
      };
      socket.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
    },
    setTimeRange(range) {
      const now = new Date().getTime();
      let startTime;

      if (range === '1D') {
        startTime = now - 24 * 60 * 60 * 1000;
      } else if (range === '1W') {
        startTime = now - 7 * 24 * 60 * 60 * 1000;
      } else if (range === '1M') {
        startTime = now - 30 * 24 * 60 * 60 * 1000;
      }

      this.chartOptions.xaxis.min = startTime;
      this.chartOptions.xaxis.max = now;
    },
    toggleLiveData() {
      this.liveData = !this.liveData;
    },
    // Reset and create a new chart
    resetChart() {
      // Reset the series data to an empty array
      this.series[0].data = [];
      
      // Trigger a re-render by updating the chart's key or calling redraw()
      this.$nextTick(() => {
        // Clear the existing data and fetch new data
        this.fetchInitialData(); // Optionally fetch new data for the chart
      });
    }
  }
};
</script>


<style>
.chart-container {
  display: flex;
  flex-direction: column;
  width: 50vw; /* Full width */
  height: 50vh; /* Full height */
  background-color: #f4f4f8;
}

.toolbar {
  display: flex;
  gap: 10px;
  padding: 10px;
  z-index: 10;
}

.toolbar button {
  padding: 8px 12px;
  font-size: 14px;
  cursor: pointer;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
}

.toolbar button:hover {
  background-color: #45a049;
}

.chart {
  flex-grow: 1; /* Ensures the chart takes the remaining space */
  width: 100%;
  height: 100%;
}
</style> -->
































<!-- <template>
  <div class="chart-container">
    <p v-if="reconnectAttempts > 0 && reconnectAttempts <= maxReconnectAttempts">กำลังเชื่อมต่อใหม่... (พยายาม {{ reconnectAttempts }}/{{ maxReconnectAttempts }})</p>
    <p v-if="reconnectAttempts === 0">WebSocket เชื่อมต่อแล้ว</p>
    <div class="toolbar">
      <button @click="setTimeRange('1D')">1D</button>
      <button @click="setTimeRange('1W')">1W</button>
      <button @click="setTimeRange('1M')">1M</button>
    </div>
    <div ref="chart" class="chart"></div>
  </div>
</template>

<script>
import { createChart } from 'lightweight-charts';
import { nextTick } from 'vue';

export default {
  data() {
    return {
      chart: null,
      candleSeries: null,
      seriesData: [], // Initial data for the chart
      timeRange: '1M', // Default time range
      reconnectAttempts: 0, // Track reconnection attempts
      maxReconnectAttempts: 10, // Limit reconnection attempts
    };
  },
  async mounted() {
    await this.initChart(); // Initialize after DOM is fully loaded
    this.fetchInitialData();
    this.connectWebSocket();
  },
  methods: {
    async initChart() {
      // Wait until the DOM is fully rendered
      await nextTick();

      this.chart = createChart(this.$refs.chart, {
        width: this.$refs.chart.clientWidth,
        height: 600,
        layout: {
          backgroundColor: '#000',
          textColor: '#333',
        },
        grid: {
          vertLines: { color: '#e1e3e6' },
          horzLines: { color: '#e1e3e6' },
        },
        timeScale: {
          timeVisible: true,
          secondsVisible: false,
        },
      });

      this.candleSeries = this.chart.addCandlestickSeries();
    },

    // Fetch initial data to populate the chart
    async fetchInitialData() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/klines/');
        const data = await response.json();

        this.seriesData = data.map(d => ({
          time: d.time,
          open: d.open,
          high: d.high,
          low: d.low,
          close: d.close,
        }));
        this.candleSeries.setData(this.seriesData);
      } catch (error) {
        console.error("Error fetching initial data:", error);
      }
    },

    // Connect WebSocket for real-time updates
    connectWebSocket() {
      const socket = new WebSocket('ws://127.0.0.1:9000/ws/klines/');

      socket.onopen = () => {
        console.log("WebSocket connection opened");
        this.reconnectAttempts = 0; // Reset reconnect attempts on successful connection
      };

      socket.onmessage = (event) => {
        try {
          console.log("data : ", event.data)
          const response = JSON.parse(event.data);
          const klines = response.klines; // Assuming 'klines' is the array containing the candlestick data

          // Ensure klines is an array and has data
          if (!Array.isArray(klines) || klines.length === 0) {
            console.error("Invalid or empty 'klines' array:", response);
            return;
          }

          // Process each kline (candlestick data)
          klines.forEach((newPoint) => {
            // Ensure that 'time' exists and is a valid number
            if (!newPoint.hasOwnProperty('time') || typeof newPoint.time !== 'number') {
              console.error("Invalid or missing 'time' property:", newPoint);
              return;
            }

            // If the time is in milliseconds, convert to seconds
            const timeInSeconds = Math.floor(newPoint.time / 1000);

            // Validate that required fields are present
            if (!newPoint.open || !newPoint.high || !newPoint.low || !newPoint.close) {
              console.error("Incomplete data received:", newPoint);
              return;
            }
            // ตรวจสอบว่า visibleRange เป็น null หรือไม่
            const visibleRange = this.chart.timeScale().getVisibleRange();
            if (visibleRange && visibleRange.to) {
              // หาก visibleRange ไม่เป็น null, อัปเดตช่วงเวลาแสดงผล
              if (timeInSeconds > visibleRange.to) {
                this.chart.timeScale().setVisibleRange({ from: visibleRange.to, to: timeInSeconds });
              }
            } else {
              // หากไม่สามารถดึง visibleRange ได้, แสดงข้อผิดพลาด
              console.error("Unable to get visible range from the chart.");
            }

            // Update the chart with new data
            this.candleSeries.update({
              time: timeInSeconds,
              open: newPoint.open,
              high: newPoint.high,
              low: newPoint.low,
              close: newPoint.close,
            })
          })
        } catch (error) {
          console.error("Error parsing WebSocket data:", error);
        }
      },

      socket.onerror = (error) => {
        console.error("WebSocket error occurred:", error.message || error);
      };

      socket.onclose = (event) => {
        if (!event.wasClean) {
          console.warn("WebSocket connection closed unexpectedly:", event);
          if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Reconnecting... (Attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            setTimeout(this.connectWebSocket, 5000); // Retry after 5 seconds
          } else {
            console.error("Max reconnection attempts reached.");
          }
        }
      };
    },

    // Set visible time range for the chart
    setTimeRange(range) {
      const now = Date.now() / 1000;
      let startTime;

      if (range === '1D') startTime = now - 86400;
      else if (range === '1W') startTime = now - 604800;
      else if (range === '1M') startTime = now - 2592000;

      this.chart.timeScale().setVisibleRange({ from: startTime, to: now });
    },
  },
};
</script>

<style scoped>
.chart-container {
  display: flex;
  flex-direction: column;
  width: 50vw;
  height: 50vh;
  background-color: #f4f4f8;
}

.toolbar {
  display: flex;
  gap: 10px;
  padding: 10px;
  z-index: 10;
}

.toolbar button {
  padding: 8px 12px;
  font-size: 14px;
  cursor: pointer;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
}

.toolbar button:hover {
  background-color: #45a049;
}

.chart {
  flex-grow: 1;
  width: 100%;
  height: 100%;
}
</style> -->
