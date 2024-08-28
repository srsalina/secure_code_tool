import React from "react";
import {Container} from 'react-bootstrap'

function Results({results}){

    return(
        <Container>
            <h1>Analysis Results</h1>
            <pre>{results}</pre>
        </Container>
    )
}

export default Results;