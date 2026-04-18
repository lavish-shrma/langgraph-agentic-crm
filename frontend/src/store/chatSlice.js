import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { sendChatMessage } from '../api/agentApi.js';
import { populateFromAgent, setAISuggestions } from './interactionSlice.js';
import { MAX_CHAT_HISTORY } from '../utils/constants.js';

const initialState = {
  messages: [],
  loading: false,
  error: null,
};

export const sendMessage = createAsyncThunk(
  'chat/sendMessage',
  async (message, { getState, dispatch, rejectWithValue }) => {
    try {
      dispatch(addMessage({ role: 'user', content: message }));

      const state = getState().chat;
      const history = state.messages.slice(-MAX_CHAT_HISTORY).map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const data = await sendChatMessage(message, history);

      dispatch(addMessage({ role: 'assistant', content: data.response }));

      // If agent extracted interaction fields, populate the form
      if (data.extracted_fields) {
        dispatch(populateFromAgent(data.extracted_fields));
      }

      if (data.partial_update) {
        dispatch(populateFromAgent(data.partial_update));
      }

      if (data.suggested_follow_ups && data.suggested_follow_ups.length > 0) {
        dispatch(setAISuggestions(data.suggested_follow_ups));
      }

      return data;
    } catch (err) {
      const respData = err.response?.data;
      const errorMsg = respData?.detail?.message || respData?.detail || respData?.message || err.message || 'Failed to get AI response';
      dispatch(addMessage({ role: 'assistant', content: `System Error: ${errorMsg}` }));
      return rejectWithValue(errorMsg);
    }
  }
);

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addMessage(state, action) {
      state.messages.push({
        id: Date.now() + Math.random(),
        role: action.payload.role,
        content: action.payload.content,
        timestamp: new Date().toISOString(),
      });
    },
    setLoading(state, action) {
      state.loading = action.payload;
    },
    clearChat() {
      return { ...initialState };
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(sendMessage.fulfilled, (state) => {
        state.loading = false;
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { addMessage, setLoading, clearChat } = chatSlice.actions;
export default chatSlice.reducer;
