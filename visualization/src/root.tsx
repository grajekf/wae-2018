import React, { Component } from "react";
import { Switch, Route, Link } from "react-router-dom";
import ObjectiveFunctionGraph from "./components/objectiveFunctionGraph";
import StatusBar from "./components/statusBar";
import ClassPredictionGraph from "./components/classPredictionGraph";
import BestSpecimenImage from "./components/bestSpecimenImage";
import PopulationGraph from "./components/populationGraph";
import AppBar from "material-ui/AppBar";
import Toolbar from "material-ui/Toolbar";
import Typography from "material-ui/Typography";
import Paper from "material-ui/Paper";
import Card, { CardHeader } from "material-ui/Card";
import { Grid, Row, Col } from "react-flexbox-grid";
import { CircularProgress } from "material-ui/Progress";
import Button from "material-ui/Button";
import { updateData, updateConnection } from "./actions";
import { VisualizationData } from "./reducers";
import { AppState } from "./reducers";
import store from "./index";
import Dialog, {
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
} from "material-ui/Dialog";
import { connect } from "react-redux";

class Root extends Component<any, any> {

    constructor(props: any) {
        super(props);
    }

    componentDidMount() {
        this.tryConnect();
    }

    tryConnect() {
        if (this.props.connected === false && this.props.connecting === false) {
            this.props.updateConnection({
                connectionFailure: false,
                connecting: true,
                connected: false
            });
            this.connect();
        }
    }


    connect(): any {
        const socket = new WebSocket("ws://localhost:3001");
        socket.onerror = err => {
            this.props.updateConnection({
                connecting: false,
                connected: false,
                connectionFailure: true
            });
        };
        socket.onmessage = msg => {
            let data = JSON.parse(msg.data) as VisualizationData;
            store.dispatch(updateData(data));
        };
        socket.onopen = event => {
            this.props.updateConnection({
                connected: true,
                connecting: false,
                connectionFailure: false
            });
        };
        socket.onclose = event => {
            if (this.props.connected) {
                this.props.updateConnection({
                    connected: false,
                    connectionFailure: false,
                    connecting: false
                });
            }
        };
    }

    render() {
        const style = {
            margin: 10,
            textAlign: "center"
        };

        return <div>
            <AppBar position="static">
                <Toolbar>
                    <Typography color="inherit">
                        WAE Visualization
                    </Typography>
                </Toolbar>
            </AppBar>
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
                    <Col xs={6}>
                        <Card style={style}>
                            <CardHeader title="Population" />
                            <PopulationGraph />
                        </Card>
                    </Col>
                </Row>
            </Grid>

            <Dialog
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
                open={this.props.connectionFailure === true}>
                <DialogTitle id="alert-dialog-title">{"Failed to connect"}</DialogTitle>
                <DialogContent>
                    Is the server working?
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => this.tryConnect()} color="primary">
                        Reconnect
                    </Button>
                </DialogActions>
            </Dialog>

            <Dialog
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
                open={!this.props.connected && !this.props.connectionFailure && !this.props.connecting}>
                <DialogTitle id="alert-dialog-title">{"Disconnected"}</DialogTitle>
                <DialogContent>
                    Is the server working?
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => this.tryConnect()} color="primary">
                        Reconnect
                    </Button>
                </DialogActions>
            </Dialog>

            <Dialog
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
                open={this.props.connecting}>
                <DialogTitle id="alert-dialog-title">{"Connecting to server"}</DialogTitle>
                <DialogContent>
                    <div style={{ display: "table", margin: "0 auto" }}>
                        <CircularProgress />
                    </div>
                </DialogContent>
            </Dialog>
        </div >;
    }
}

function mapStateToProps(appState: AppState) {
    console.log(appState.connectionState);
    return {
        ...appState.connectionState
    };
}

export default connect(mapStateToProps, { updateData, updateConnection })(Root);

