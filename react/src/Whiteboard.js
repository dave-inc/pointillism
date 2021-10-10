import React, { Component } from 'react';
import TextField from '@material-ui/core/TextField';

class Whiteboard extends Component {
    constructor(props) {
        super(props);
        this.state = {
            'board': "digraph G { pointillism -> {you, friends} }"
        }
        this.onChange = this.onChange.bind(this);
    }

    onChange(event) {
        const newVal = event.target.value;
        if (this.board !== this.state.board) {
            this.present(newVal, this)
        }
        this.setState({ 'board': newVal });
    }

    present(payload, self) { // render and display image
        try {
            fetch("/render", {
                method: "post",
                headers: {
                    'Content-Type': 'application/dot'
                },
                body: payload,
            }).then(function (resp) {
                return resp.text();
                // }).then(function (data) {
                //     return import(data);
            }).then(function (svgfile) {
                console.log(svgfile)

                self.setState({ 'image': `data:image/svg+xml;base64,${btoa(svgfile)}` });
            });
        }
        catch (err) {
            return '';
        }
    }

    render() {
        let rendering = '';
        if (this.state.image) {
            rendering = <img src={this.state.image} alt="pointillism.io rendered" />;
        }

        return (
            <div>
                <TextField
                    name="board"
                    multiline
                    value={this.state.board}
                    rows="4"
                    label="DOT Graph Source"
                    fullWidth="true"
                    onChange={this.onChange}
                //onPaste={this.paste} 
                />
                <div class="center">
                    {rendering}
                </div>
            </div>
        )
    }
}

export default Whiteboard
