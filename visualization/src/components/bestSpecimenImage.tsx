import React, { Component } from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { Line } from "react-chartjs-2";
import { AppState, VisualizationData, ConnectionState } from "../reducers";

class BestSpecimenImage extends Component<any, any> {

    constructor(props: any) {
        super(props);
        this.state = {};
    }

    render() {
        return <div style={{ width: "100%", margin: "0 auto" }}>
            <img style={{ height: "100%", margin: "0 auto" }} src={`data:image/png;base64, ${this.props.image}`} />
        </div>;
    }

}

function mapStateToProps(appState: AppState) {
    return {
        image: appState.visualizationData.bestSpecimenData.image
    };
}

export default connect(mapStateToProps, {})(BestSpecimenImage);


