import axiosClient from './axiosClient.js';

export async function sendChatMessage(message, conversationHistory = []) {
  const response = await axiosClient.post('/api/agent/chat', {
    message,
    conversation_history: conversationHistory,
  });
  return response.data;
}
