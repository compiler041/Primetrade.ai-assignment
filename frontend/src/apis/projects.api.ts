import { PartialProject } from "../types/Project";

const BASE_URL = process.env.REACT_APP_BASE_API_URL || "";

function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem("token");
  return token
    ? { "Content-Type": "application/json", Authorization: `Bearer ${token}` }
    : { "Content-Type": "application/json" };
}

function getAuthHeadersNoContent(): HeadersInit {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export function getProjectTasks(projectId: number, signal?: AbortSignal) {
  return fetch(`${BASE_URL}/projects/${projectId}/tasks`, {
    signal: signal,
    headers: getAuthHeadersNoContent(),
  });
}

export function createProject(project: PartialProject, signal?: AbortSignal) {
  return fetch(`${BASE_URL}/projects`, {
    method: "POST",
    signal: signal,
    headers: getAuthHeaders(),
    body: JSON.stringify(project),
  });
}

export function updateProject(
  projectId: number,
  project: PartialProject,
  signal?: AbortSignal
) {
  return fetch(`${BASE_URL}/projects/${projectId}`, {
    method: "PUT",
    signal: signal,
    headers: getAuthHeaders(),
    body: JSON.stringify(project),
  });
}

export function deleteProject(projectId: number, signal?: AbortSignal) {
  return fetch(`${BASE_URL}/projects/${projectId}`, {
    method: "DELETE",
    signal: signal,
    headers: getAuthHeadersNoContent(),
  });
}

export function getProjects(signal?: AbortSignal) {
  return fetch(`${BASE_URL}/projects`, {
    signal: signal,
    headers: getAuthHeadersNoContent(),
  });
}