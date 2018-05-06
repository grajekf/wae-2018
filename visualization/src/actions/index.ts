import { VisualizationData } from "../reducers";
import { Dispatch } from "redux";
import store from "..";
export enum ActionType {
    UPDATE,
    CONNECT
}

export function updateData(data: VisualizationData): any {
    const promise = new Promise<any>((resolve, reject) => {
        resolve(data);
    });
    return {
        type: ActionType.UPDATE,
        payload: promise
    };
}

export function connect(updateState: (data: VisualizationData) => void): any {
    const promise = new Promise<any>((resolve, reject) => {
        const socket = new WebSocket("ws://localhost:3001");
        socket.onerror = err => {
            console.error(err);
            reject(err);
        };
        socket.onmessage = msg => {
            let data = JSON.parse(msg.data) as VisualizationData;
            store.dispatch(updateData(data));
        };
        socket.onopen = event => {
            console.log("connection established");
            console.log(event);
            resolve(event);
        };
        socket.onclose = event => {
            console.log("connection closed");
            console.log(event);
        };
    });
    return {
        type: ActionType.CONNECT,
        payload: promise
    };
}
