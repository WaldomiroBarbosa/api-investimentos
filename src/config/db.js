const { Pool } = require('pg');

async function connection ()
{
    if(global.connection)
        return global.connection.connect();

    const pool = new Pool ({
        connectionString: process.env.CONNECTION_STRING
    });

    //apenas testando a conexão
    const client = await pool.connect();
    console.log("Criou pool de conexões no PostgreSQL!");
 
    const res = await client.query('SELECT NOW()');
    console.log(res.rows[0]);
    client.release();

    global.connection = pool;
    return pool.connect();
}

connection();

async function selectClients() 
{
    const client = await connection();
    const res = await client.query('SELECT * FROM client');
    return res.rows;
}

async function selectClient(id) 
{
    const client = await connection();
    const res = await client.query('SELECT * FROM client WHERE id=$1', [id]);
    return res.rows;
}

async function deleteClient(id) 
{
    const client = await connection();
    return await client.query('DELETE FROM client where id=$1;', [id]);
}
 
async function insertClient(bdclient) 
{
    const client = await connection();
    const sql = 'INSERT INTO client(name,email,phone_number,user_profile) VALUES ($1,$2,$3, $4);';
    const values = [bdclient.nome, bdclient.email, bdclient.phone_number,bdclient.user_profile];
    return await client.query(sql, values);
}

async function updateClient(id, bdclient) 
{
    const client = await connection();
    const sql = 'UPDATE client SET name=$1, email=$2, phone_number=$3, user_profile=$4 WHERE id=$5';
    const values = [bdclient.nome, bdclient.email, bdclient.phone_number,bdclient.user_profile, id];
    return await client.query(sql, values);
}

async function insertStock(stock)
{
    const client = await connection();
    const sql = 'INSERT INTO STOCK(name,sector,stock_profile) VALUES ($1,$2,$3);';
    const values = [stock.name, stock.sector, stock.stock_profile];
    return await client.query(sql,values);
}

async function selectStock(id)
{
    const client = await connection();
    const res = await client.query('SELECT * FROM stock WHERE id=$1', [id]);
    return res.rows;
}

async function selectStocks()
{
    const client = await connection();
    const res = await client.query('SELECT * FROM stock');
    return res.rows;
}

async function insertClientInterest(stock_client)
{
    const client = await connection();
    const sql = 'INSERT INTO client_stock(client_id,stock_id,interest) VALUES ($1,$2,$3);';
    const values = [stock_client.client_id, stock_client.stock_id, stock_client.interest];
    return await client.query(sql,values);
}

module.exports = { selectClients, selectClient, deleteClient, insertClient, updateClient, insertStock, selectStock, selectStocks, insertClientInterest }