import React, { Component } from "react";
import { Switch, Route, Link } from "react-router-dom";
import ObjectiveFunctionGraph from "./components/objectiveFunctionGraph";
import StatusBar from "./components/statusBar";
import ClassPredictionGraph from "./components/classPredictionGraph";
import BestSpecimenImage from "./components/bestSpecimenImage";
import AppBar from "material-ui/AppBar";
import Paper from "material-ui/Paper";
import { Card, CardHeader } from "material-ui/Card";
import { Grid, Row, Col } from "react-flexbox-grid";
import { RaisedButton } from "material-ui";
import { connect as websocketConnect, updateData } from "./actions";
import { AppState } from "./reducers";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";

class Root extends Component<any, any> {

    componentDidMount() {
        console.log("component did mount");
        websocketConnect(this.props.updateData);
    }

    render() {
        const style = {
            margin: 10,
            textAlign: "center"
        };

        return <div>
            <AppBar title="WAE Visualization" showMenuIconButton={false} />
            <Grid fluid>
                <Row>
                    <Col xs={6}>
                        <Card style={style}>
                            <CardHeader title="Class prediction" />
                            <ClassPredictionGraph />
                        </Card>
                    </Col>
                    <Col xs={6}>
                        <Card style={style}>
                            <CardHeader title="Objective function" />
                            <ObjectiveFunctionGraph />
                        </Card>
                    </Col>
                </Row>
                <Row>
                    <Col xs={6}>
                        <Card style={style}>
                            <CardHeader title="Best image" />
                            <BestSpecimenImage />
                        </Card>
                    </Col>
                    {/* <Col xs={6}>
                        <Card style={style}>
                            <CardHeader title="Status" />
                            <StatusBar />
                        </Card>
                    </Col> */}
                </Row>
            </Grid>
        </div >;
    }
}

function mapStateToProps(appState: AppState) {
    return {

    };
}

export default connect(mapStateToProps, { updateData, websocketConnect })(Root);

