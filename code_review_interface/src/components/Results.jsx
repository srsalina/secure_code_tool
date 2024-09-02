import React from "react";
import { Container } from 'react-bootstrap';

function Results({ results }) {
  try {
    // Check if results are available
    if (!results) {
      return (
        <Container>
          <h1>Analysis Results</h1>
          <p>No results to display. Please upload a Python file and try again.</p>
        </Container>
      );
    }

    // Render the results, handling both string and object types
    return (
      <Container>
        <h1>Analysis Results</h1>
        {typeof results === 'string' ? (
          <pre>{results}</pre>  // Display plain text results
        ) : (
          <pre>{JSON.stringify(results, null, 2)}</pre>  // Display formatted JSON results
        )}
      </Container>
    );

  } catch (error) {
    console.error("Error rendering results:", error);  // Log error for debugging
    return (
      <Container>
        <h1>Analysis Results</h1>
        <p>There was an error displaying the results. Please try again.</p>
      </Container>
    );
  }
}

export default Results;
