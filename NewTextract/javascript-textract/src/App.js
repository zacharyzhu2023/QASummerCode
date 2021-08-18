import logo from './logo.svg';
import './App.css';
// import {promises as fs} from 'fs';
// import { TextractClient, AnalyzeDocumentCommand } from "@aws-sdk/client-textract";
import AWS from 'aws-sdk';
const fs = require('fs');
const reader = new FileReader()
var canvas = document.getElementById("canvas");;
const testTextract = async() => {
  try {
    const test = 5;
    console.log('LOG1');
    const {TextractClient, AnalyzeDocumentCommand} = require("@aws-sdk/client-textract")
    const client = new TextractClient({region: 'us-east-1'});
    // const buf = await fs.readFile('./example.png');
    console.log('LOG1');

    const buf = await fs.readFile('example.png');
    console.log('LOG2');
    

  } catch (err) {
    console.log(err);
  }
}

function App() {
  return (
    <div className="App">
      Text Display
    </div>
  );
}

testTextract();


export default App;
