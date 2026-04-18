import axiosClient from './axiosClient.js';

export async function createInteraction(data) {
  const response = await axiosClient.post('/api/interactions', data);
  return response.data;
}

export async function getInteractions({ hcp_id, limit = 10, offset = 0 } = {}) {
  const params = { limit, offset };
  if (hcp_id) params.hcp_id = hcp_id;
  const response = await axiosClient.get('/api/interactions', { params });
  return response.data;
}

export async function getInteractionById(id) {
  const response = await axiosClient.get(`/api/interactions/${id}`);
  return response.data;
}

export async function updateInteraction(id, data) {
  const response = await axiosClient.put(`/api/interactions/${id}`, data);
  return response.data;
}
