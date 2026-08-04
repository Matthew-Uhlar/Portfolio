import * as signalR from '@microsoft/signalr'
import { getToken } from './api'

export function createIncidentConnection() {
  return new signalR.HubConnectionBuilder()
    .withUrl('/hubs/incidents', {
      accessTokenFactory: () => getToken() ?? ''
    })
    .withAutomaticReconnect()
    .build()
}
