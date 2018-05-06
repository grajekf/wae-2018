import React, { Component } from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { Line } from "react-chartjs-2";
import { AppState, VisualizationData, ConnectionState } from "../reducers";

class ObjectiveFunctionGraph extends Component<any, any> {

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
                },
                {
                    label: "Best",
                    fill: false,
                    borderColor: "green",
                    data: this.props.best
                },
                {
                    label: "Median",
                    fill: false,
                    borderColor: "blue",
                    data: this.props.median
                },
                {
                    label: "Worst",
                    fill: false,
                    borderColor: "black",
                    data: this.props.worst
                }
            ]
        };

        return <div>
            <Line data={data} options={{
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: "Objective function value",
                            fontSize: 18
                        }
                    }],
                    xAxes: [
                        {
                            scaleLabel: {
                                display: true,
                                labelString: "Generation",
                                fontSize: 18
                            }
                        }
                    ]
                },
                pan: {
                    // Boolean to enable panning
                    enabled: true,

                    // Panning directions. Remove the appropriate direction to disable
                    // Eg. 'y' would only allow panning in the y direction
                    mode: "xy"
                },
                zoom: {
                    // Boolean to enable zooming
                    enabled: true,

                    // Enable drag-to-zoom behavior
                    drag: true,
                    mode: "xy"
                }
            }} />
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

export default connect(mapStateToProps, {})(ObjectiveFunctionGraph);
