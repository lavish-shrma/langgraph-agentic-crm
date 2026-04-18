import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { searchHcpsApi, getHcpById } from '../api/hcpApi.js';

const initialState = {
  hcps: [],
  selectedHCP: null,
  loading: false,
  error: null,
};

export const searchHCPs = createAsyncThunk(
  'hcp/search',
  async (query, { rejectWithValue }) => {
    try {
      const data = await searchHcpsApi(query);
      return data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.detail || 'Failed to search HCPs');
    }
  }
);

export const fetchHCP = createAsyncThunk(
  'hcp/fetch',
  async (hcpId, { rejectWithValue }) => {
    try {
      const data = await getHcpById(hcpId);
      return data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.detail || 'Failed to fetch HCP');
    }
  }
);

const hcpSlice = createSlice({
  name: 'hcp',
  initialState,
  reducers: {
    setHCPs(state, action) {
      state.hcps = action.payload;
    },
    setSelectedHCP(state, action) {
      state.selectedHCP = action.payload;
    },
    clearHCPs(state) {
      state.hcps = [];
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(searchHCPs.pending, (state) => {
        state.loading = true;
      })
      .addCase(searchHCPs.fulfilled, (state, action) => {
        state.loading = false;
        state.hcps = action.payload;
      })
      .addCase(searchHCPs.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchHCP.fulfilled, (state, action) => {
        state.selectedHCP = action.payload;
      });
  },
});

export const { setHCPs, setSelectedHCP, clearHCPs } = hcpSlice.actions;
export default hcpSlice.reducer;
