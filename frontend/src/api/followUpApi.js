import axiosClient from './axiosClient.js';

export async function createFollowUpApi(data) {
  const response = await axiosClient.post('/api/follow-ups', data);
  return response.data;
}

export async function getFollowUpsApi(hcpId, status) {
  const params = {};
  if (hcpId) params.hcp_id = hcpId;
  if (status) params.status = status;
  const response = await axiosClient.get('/api/follow-ups', { params });
  return response.data;
}

export async function updateFollowUpApi(id, data) {
  const response = await axiosClient.put(`/api/follow-ups/${id}`, data);
  return response.data;
}
