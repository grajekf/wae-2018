import React, { Component } from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { Bar } from "react-chartjs-2";
import { AppState, VisualizationData, ConnectionState } from "../reducers";

class ClassPredictionGraph extends Component<any, any> {

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
                    backgroundColor: ["red", "green", "blue", "yellow", "black"],
                    borderWidth: 1,
                    data: this.props.probabilities
                }
            ],

        };
        const options = {
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        min: 0
                    },
                    scaleLabel: {
                        display: true,
                        labelString: "Probability",
                        fontSize: 18
                    }
                }],
                xAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: "Class name",
                            fontSize: 18
                        }
                    }
                ]
            }
        };

        return <div>
            <Bar
                data={data}
                options={options}
            />
        </div>;
    }

}

function mapStateToProps(appState: AppState) {
    return {
        labels: appState.visualizationData.bestSpecimenData.predictions.map(p => p.className.toUpperCase()),
        probabilities: appState.visualizationData.bestSpecimenData.predictions.map(p => p.probability)
    };
}

export default connect(mapStateToProps, {})(ClassPredictionGraph);
