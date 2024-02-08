// pages/api/getResult.js
import { exec } from 'child_process';

// Set your OpenAI API key as an environment variable
// const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
// if (!OPENAI_API_KEY) {
//   console.error('OPENAI_API_KEY is not set. Please set your API key.');
//   process.exit(1);
// }


// // run embedText.py
// const { spawn } = require('child_process');

// const pythonProcess = spawn('python3', ['embedText.py']);
// pythonProcess.on('close', (code) => {
//   if (code === 0) {
//     console.log('Python Script Execution Successful');
//   } else {
//     console.error(`Python Script Execution Failed with Code ${code}`);
//   }
// });

export default (req, res) => {

  if (req.method === 'GET') {
    const question = req.query.question || ''; // Default to 0 if parameter is not provided

    // Execute the Python script with the provided parameter
    exec(`python3 script.py ${question}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing Python script: ${error}`);
        res.status(500).json({ result: 'Internal Server Error' });
        return;
      }

      const result = stdout.trim();
      console.log(result) // log the result in console

      // Send the result as JSON
      res.status(200).json({ result });
    });
  } else {
    res.status(405).end(); // Method Not Allowed for non-GET requests
  }
};
