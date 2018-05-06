import { combineReducers } from "redux";
import { ActionType } from "../actions";

export interface AppState {
    visualizationData: VisualizationData;
    connectionState: ConnectionState;
}

export interface ConnectionState {
    socket: WebSocket | null;
}

export interface VisualizationData {
    generation: number;
    currentAction: string;
    objectiveFunctionData: {
        best: number[],
        worst: number[],
        mean: number[],
        median: number[]
    };
    bestSpecimenData: {
        image: string;
        predictions: { className: string, probability: number }[];
    };
}

const rootReducer = combineReducers(
    {
        visualizationData: visualizationDataReducer,
        connectionState: connectionStateReducer
    }
);

export function connectionStateReducer(state: ConnectionState = { socket: null }, action: any): ConnectionState {
    switch (action.type) {
        default:
            return state;
    }
}

export function visualizationDataReducer(state: VisualizationData = {
    generation: 0,
    currentAction: "Creating next generation",
    objectiveFunctionData: {
        best: [],
        worst: [],
        mean: [],
        median: []
    },
    bestSpecimenData: {
        image: "",
        predictions: []
    },
}, action: any): VisualizationData {
    console.log(action);
    switch (action.type) {
        case ActionType.UPDATE:
            console.log("updating payload");
            console.log(action);
            return action.payload;
        default:
            return state;
    }
}

export default rootReducer;
