const express = require("express");
const router = express.Router();
const db = require("./config/db");


router.post("/add", async (request, response) => 
    {
        const { user, email, phone_number, user_profile } = request.body;
    
        try 
        {
            await db.insertClient(req.body);
            res.sendStatus(201);
        } catch (err) {
            console.error(err);
            response.status(500).json({ error: "Erro ao criar o cliente:", err });
        }
    })
    
router.put("/update/:id", async (request, response) =>
    {
        const { user_id } = request.body;
    
        try 
        {
            await db.updateClient(req.params.id, req.body);
            res.sendStatus(200);
        } catch (err) {
            console.error(err);
            response.status(500).json({ error: "Erro ao alterar o cliente:", err });
        }
    })
    
router.delete("/delete/:id", async (request, response) =>
    {
        const { user_id } = request.body;
    
        try
        {
            await db.deleteCustomer(req.params.id);
            res.sendStatus(204);
        } catch (err) {
            console.error(err);
            response.status(500).json({ error: "Erro ao deletar o cliente:", err });
        }
    })
    
router.get("/all", async (request, response) =>
    {
        try
        {
            const clients = await db.selectClients();
            response.status(200).json(clients);
        } catch (err) {
            console.error(err);
            response.status(500).json({ error: "Erro ao obter os clientes:", err });
        }
        
    })
    
router.get('/:id', async (req, res) => 
    { 
        try
        {
            const customer = await db.selectClient(req.params.id);
            res.status(200).json(customer);
        } catch (err) {
            console.error(err);
            response.status(500).json({ error: "Erro ao obter o cliente:", err });
        }
        
    })

modules.export = router;