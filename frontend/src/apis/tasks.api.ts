import { PartialTask } from "../types/Task";

const BASE_URL = process.env.REACT_APP_BASE_API_URL || "";

function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem("token");
  return token
    ? { "Content-Type": "application/json", Authorization: `Bearer ${token}` }
    : { "Content-Type": "application/json" };
}

export function createTask(task: PartialTask, signal?: AbortSignal) {
  return fetch(`${BASE_URL}/tasks`, {
    method: "POST",
    signal: signal,
    headers: getAuthHeaders(),
    body: JSON.stringify(task),
  });
}

export function updateTask(
  taskId: number,
  task: PartialTask,
  signal?: AbortSignal
) {
  return fetch(`${BASE_URL}/tasks/${taskId}`, {
    method: "PUT",
    signal: signal,
    headers: getAuthHeaders(),
    body: JSON.stringify(task),
  });
}

export function deleteTask(taskId: number, signal?: AbortSignal) {
  return fetch(`${BASE_URL}/tasks/${taskId}`, {
    method: "DELETE",
    signal: signal,
    headers: getAuthHeaders(),
  });
}

export function getTasks(signal?: AbortSignal) {
  return fetch(`${BASE_URL}/tasks`, {
    signal: signal,
    headers: getAuthHeaders(),
  });
}
