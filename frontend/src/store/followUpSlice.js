import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { createFollowUpApi, getFollowUpsApi } from '../api/followUpApi.js';

const initialState = {
  followUps: [],
  loading: false,
  error: null,
};

export const addFollowUp = createAsyncThunk(
  'followUp/add',
  async (followUpData, { rejectWithValue }) => {
    try {
      const data = await createFollowUpApi(followUpData);
      return data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.detail || 'Failed to create follow-up');
    }
  }
);

export const fetchFollowUps = createAsyncThunk(
  'followUp/fetch',
  async ({ hcpId, status } = {}, { rejectWithValue }) => {
    try {
      const data = await getFollowUpsApi(hcpId, status);
      return data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.detail || 'Failed to fetch follow-ups');
    }
  }
);

const followUpSlice = createSlice({
  name: 'followUp',
  initialState,
  reducers: {
    setFollowUps(state, action) {
      state.followUps = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(addFollowUp.pending, (state) => {
        state.loading = true;
      })
      .addCase(addFollowUp.fulfilled, (state, action) => {
        state.loading = false;
        state.followUps.push(action.payload);
      })
      .addCase(addFollowUp.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchFollowUps.fulfilled, (state, action) => {
        state.followUps = action.payload;
      });
  },
});

export const { setFollowUps } = followUpSlice.actions;
export default followUpSlice.reducer;
