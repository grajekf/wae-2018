import React, { Component } from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { Scatter } from "react-chartjs-2";
import { AppState, VisualizationData, ConnectionState } from "../reducers";
const Plot = require("react-plotly.js");

class PopulationGraph extends Component<any, any> {

    constructor(props: any) {
        super(props);
        this.state = {
        };
    }

    render() {
        const data = {
            datasets: [
                {
                    borderColor: "red",
                    data: this.props.data
                }
            ]
        };

        return <div style={{ margin: "0 auto", display: "flex" }}>
            <Scatter data={data} options={{
                legend: {
                    display: false
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            min: -1000,
                            max: 1000
                        }
                    }],
                    xAxes: [{
                        ticks: {
                            min: -1000,
                            max: 1000
                        }
                    }]
                }

            }} />
        </div>;
    }

}

function mapStateToProps(appState: AppState) {
    return {
        data: appState.visualizationData.population
    };
}

export default connect(mapStateToProps, {})(PopulationGraph);
