import React, { Component } from 'react';
import axios from 'axios';
import logo from './logo.svg';
import './App.css';

class App extends Component {

  state = {
    users: []
  }

  getUsers = () => {
    const url = `${process.env.REACT_APP_SERVER_URL}/users`
    axios.get(url)
    .then((res) => {
      this.setState({
        'users':res.data.users
      })
    })
    .catch((err) => {
      console.log(err);
    })
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <button
            onClick={this.getUsers}
          >
            Get Users
          </button>
          <div className="userData">
            <code>{JSON.stringify(this.state.users)}</code>
          </div>
        </header>
      </div>
    );
  }
}

export default App;
