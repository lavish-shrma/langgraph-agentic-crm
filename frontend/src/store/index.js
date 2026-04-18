import { configureStore } from '@reduxjs/toolkit';
import interactionReducer from './interactionSlice.js';
import chatReducer from './chatSlice.js';
import hcpReducer from './hcpSlice.js';
import followUpReducer from './followUpSlice.js';

export const store = configureStore({
  reducer: {
    interaction: interactionReducer,
    chat: chatReducer,
    hcp: hcpReducer,
    followUp: followUpReducer,
  },
});
