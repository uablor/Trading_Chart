// stores/tradeStore.ts
import { defineStore } from "pinia";

interface Trade {
  order_type: string;
  symbol: string;
  price: number;
}

interface TradeState {
  pendingTrade: Trade | null;
  tradeResult: any | null; // store the result from backend
  isProcessing: boolean; // indicate if the request is being processed
}

export const useTradeStore = defineStore("tradeStore", {
  state: (): TradeState => ({
    pendingTrade: null,
    tradeResult: null,
    isProcessing: false,
  }),
  actions: {
    setPendingTrade(trade: Trade) {
      this.pendingTrade = trade;
      this.isProcessing = true;
    },
    setTradeResult(result: any) {
      this.tradeResult = result;
      this.isProcessing = false;
    },
    clearPendingTrade() {
      this.pendingTrade = null;
      this.tradeResult = null;
      this.isProcessing = false;
    },
  },
});
