import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { createInteraction } from '../api/interactionApi.js';

const initialState = {
  hcp_id: null,
  hcp_name: '',
  interaction_type: '',
  date: '',
  time: '',
  attendees: '',
  topics_discussed: '',
  materials_shared: [],
  samples: [],
  sentiment: '',
  outcome: '',
  follow_up_notes: '',
  follow_up_date: '',
  ai_suggested_followups: [],
  location: '',
  source: 'form',
  submitting: false,
  submitError: null,
  submitSuccess: false,
  lastInteractionId: null,
};

export const submitInteraction = createAsyncThunk(
  'interaction/submit',
  async (_, { getState, rejectWithValue }) => {
    try {
      const state = getState().interaction;
      const payload = {
        hcp_id: state.hcp_id,
        interaction_type: state.interaction_type,
        date: state.date,
        time: state.time || null,
        attendees: state.attendees || null,
        topics_discussed: state.topics_discussed || null,
        materials_shared: state.materials_shared.length > 0 ? state.materials_shared : null,
        sentiment: state.sentiment || null,
        outcome: state.outcome || null,
        follow_up_notes: state.follow_up_notes || null,
        follow_up_date: state.follow_up_date || null,
        ai_suggested_followups: state.ai_suggested_followups.length > 0 ? state.ai_suggested_followups : null,
        location: state.location || null,
        source: state.source,
        samples: state.samples.filter(s => s.product_name && s.quantity),
      };
      const data = await createInteraction(payload);
      return data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.detail || 'Failed to save interaction');
    }
  }
);

const interactionSlice = createSlice({
  name: 'interaction',
  initialState,
  reducers: {
    setField(state, action) {
      const { field, value } = action.payload;
      state[field] = value;
    },
    setAISuggestions(state, action) {
      state.ai_suggested_followups = action.payload;
    },
    populateFromAgent(state, action) {
      const fields = action.payload;
      Object.keys(fields).forEach((key) => {
        if (key in state) {
          state[key] = fields[key];
        }
      });
      state.source = 'chat';
    },
    resetForm() {
      return { ...initialState };
    },
    clearSubmitStatus(state) {
      state.submitError = null;
      state.submitSuccess = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(submitInteraction.pending, (state) => {
        state.submitting = true;
        state.submitError = null;
        state.submitSuccess = false;
      })
      .addCase(submitInteraction.fulfilled, (state, action) => {
        state.submitting = false;
        state.submitSuccess = true;
        state.lastInteractionId = action.payload.id;
      })
      .addCase(submitInteraction.rejected, (state, action) => {
        state.submitting = false;
        state.submitError = action.payload;
      });
  },
});

export const { setField, setAISuggestions, populateFromAgent, resetForm, clearSubmitStatus } = interactionSlice.actions;
export default interactionSlice.reducer;
