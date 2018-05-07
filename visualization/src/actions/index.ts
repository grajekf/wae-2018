import { VisualizationData, ConnectionState } from "../reducers";
import { Dispatch } from "redux";
import store from "..";
export enum ActionType {
    UPDATE,
    CONNECTION
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

export function updateConnection(data: ConnectionState): any {
    return {
        type: ActionType.CONNECTION,
        payload: data
    };
}

