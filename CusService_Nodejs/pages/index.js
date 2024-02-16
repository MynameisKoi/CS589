// pages/index.js
import Head from "next/head";
import { useState } from "react";
import styles from "./index.module.css";

function Home() {
  // const [parameter, setParameter] = useState(0);
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState();

  const handleClick = () => {
    // Fetch data from the Python script when the button is clicked
    fetch(`/api/getResult?question=${encodeURIComponent(question)}`)
    // fetch(`/api/getResult?parameter=${parameter}`)
      .then((response) => response.json())
      .then((data) => {
        setResult(data.result);
      });
  };

  return (
    <div>
      <Head>
        <title>OpenAI Quickstart</title>
        <link rel="icon" href="/dog.png" />
      </Head>

      <main className={styles.main}>
        <img src="/dog.png" className={styles.icon} />
        <h3>OpenAI Q&A</h3>

          <input
            type="text"
            placeholder="Enter question about openAI"
            // value={parameter}
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button onClick={handleClick}> Generate Answer </button>

      {result !== null && (
        <div className={styles.result}>{result}</div>
      )}
      </main>
    </div>
  );
}

export default Home;