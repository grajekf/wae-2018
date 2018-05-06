import React, { Component } from "react";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { AppState, VisualizationData, ConnectionState } from "../reducers";
import RaisedButton from "material-ui/RaisedButton";
import { updateData } from "../actions";

class StatusBar extends Component<any, any> {

    constructor(props: any) {
        super(props);
        this.state = {
        };
    }

    render() {
        return <div>
            {"Doing stuff"}
        </div>;
    }

}

function mapStateToProps(appState: AppState) {
    return {

    };
}

export default connect(mapStateToProps, { updateData })(StatusBar);
