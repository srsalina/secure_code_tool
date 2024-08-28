import React, {useState} from 'react';

import {Container, Form, Button} from 'react-bootstrap';


function UploadFile({onUpload}){
    let [file,setFile] = useState(null)

    const handleFileChange = e =>{
        setFile(e.target.files[0])
    }

    const handleSubmit = e => {
        e.preventDefault()

        if(file){
            const formData = new FormData();
            formData.append('file', file)
            onUpload(formData)
        }
    }

    return (
        <Container>
            <h1>Upload Python File for Secure Code Analysis</h1>
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="formFile" className="labelParent">
                    <Form.Label>
                        Select a Python File
                    </Form.Label>
                    <Form.Control type="file" accept='.py' onChange={handleFileChange} required/>
                </Form.Group>
                <Button variant='primary' type='submit'>
                    Analyze
                </Button>
            </Form>
        </Container>
    )
}

export default UploadFile