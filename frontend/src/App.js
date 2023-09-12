//import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
//import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import {
  BrowserRouter as Router,
  Route,
} from "react-router-dom";
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'


function App() {
  return (
      <Router>
          <Route exact path="/" component={HomePage} />
          <Route exact path="/login" component={LoginPage} />
      </Router>
  );
}

export default App;
