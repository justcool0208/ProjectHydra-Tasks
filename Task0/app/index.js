const express = require("express")
const app = express()
const PORT = 3000

app.get("/",(req,res)=>
{
    res.send("test message")
})

app.get("/health", (req, res) => 
{
  res.status(200).send("OK")
})


app.listen(PORT,
    ()=>
    {
        console.log("server is running at port : ",PORT)
    }
)
