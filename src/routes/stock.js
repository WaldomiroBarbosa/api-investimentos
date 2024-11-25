const express = require("express");
const router = express.Router();
const db = require("./config/db");

router.post('/add', async (req, res) =>
{
    const { name, stock, stock_profile } = res.body;
    try
    {
        const stock = await db.insertStock(req.body);
        res.status(200).json(stock);
    } catch {
        console.error(err);
        response.status(500).json({ error: "Erro ao criar a acao:", err });
    }
})
    
router.get('/:id', async (req, res) =>
{
    try
    {
        const stock = await db.selectStock(req.params.id);
        res.status(200).json(stock);
    } catch {
        console.error(err);
        response.status(500).json({ error: "Erro ao encontrar a acao:", err });
    }
})
        
router.get('/all', async (req, res) =>
{
    try
    {
            const stock = await db.selectStocks();
            res.status(200).json(stock);
    } catch {
            console.error(err);
            response.status(500).json({ error: "Erro ao encontrar as acoes:", err });
    }
})

router.post('/client', async (req, res) =>
{
    const { client_id, stock_id, interest } = req.body;

    try
    {
            const clientInterest = await db.insertClientInterest(req.body);
            res.status(200).json(stock);
    } catch {
            console.error(err);
            response.status(500).json({ error: "Erro ao inserir interesse do cliente:", err });
    }
})
            
modules.export = router;