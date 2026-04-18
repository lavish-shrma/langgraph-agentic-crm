import axiosClient from './axiosClient.js';

export async function searchHcpsApi(query = '') {
  const response = await axiosClient.get('/api/hcps', { params: { search: query } });
  return response.data;
}

export async function getHcpById(id) {
  const response = await axiosClient.get(`/api/hcps/${id}`);
  return response.data;
}
