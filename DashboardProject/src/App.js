import './App.css';
import Sidebar from './components/Sidebar';
import { BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Form from './pages/Form';
import Settings from './pages/Settings';
import Topbar from './components/Topbar';
import SignIn from './pages/SignIn';

function App() {
  return (
    <div>
      <Router>
        <Topbar />
        <Sidebar />
        <div className='container'>
          <Switch>
              <Route path='/' exact component={Dashboard} />
              <Route path='/signin' component={SignIn} />
              <Route path='/form' component={Form} />
              <Route path='/settings' component={Settings} />
          </Switch>
        </div>
      </Router>
    </div>
  );
}

export default App;
