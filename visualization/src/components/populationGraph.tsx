import React, { Component } from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { Scatter } from "react-chartjs-2";
import { AppState, VisualizationData, ConnectionState } from "../reducers";

class PopulationGraph extends Component<any, any> {

    constructor(props: any) {
        super(props);
        this.state = {
        };
    }

    render() {
        const data = {
            labels: this.props.labels,
            datasets: [
                {
                    label: "Mean",
                    fill: false,
                    borderColor: "red",
                    data: this.props.mean
                }
            ]
        };

        return <div>
            <Scatter data={data} options={{}} />
        </div>;
    }

}

function mapStateToProps(appState: AppState) {
    const labels = [...Array(appState.visualizationData.generation).keys()].map(k => k + 1);
    return {
        labels: labels,
        ...appState.visualizationData.objectiveFunctionData
    };
}

export default connect(mapStateToProps, {})(PopulationGraph);
