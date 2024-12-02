require('dotenv').config();

const cors = require('cors');
const express = require('express');
const db = require("./config/db");


const app = express();
app.use(express.json());

app.use(cors({
    origin: 'http://localhost:3456', // Origem permitida
    credentials: true               // Permite envio de cookies
}));

app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "http://localhost:3456"); // Origem permitida
    res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
    res.header("Access-Control-Allow-Headers", "Content-Type, Authorization");
    res.header("Access-Control-Allow-Credentials", "true");
    next();
});

const PORT = process.env.PORT;

app.listen(PORT, () => 
{
    console.log("Server listening on PORT: ", PORT);
});


app.get("/status", (request, response) =>
{
    const status = 
    {
        "Status": "Running"
    };

    response.send(status);
});

const clientRoute = require('./routes/client')
const stockRoute = require('./routes/stock')
app.use("/client", clientRoute);
app.use("/stock", stockRoute)



