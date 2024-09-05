const express = require("express");
const axios = require("axios");
const { GoogleGenerativeAI } = require("@google/generative-ai");
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

const genAI = new GoogleGenerativeAI(process.env.API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
const accessKey = process.env.ACCESS_KEY || "GLIMMERTEMP";

app.post("/api/v1/endpoints/shimmer", async (req, res) => {
  if (req.body.accessKey == accessKey) {
    try {
      const result = await model.generateContent(req.body.prompt);
      console.log(result.response.text());
      res.json(result.response);
    } catch (error) {
      res.status(500).send(error.toString());
    }
  } else {
    res.status(403).send("403 Forbidden");
  }
});

app.listen(port, () => {
  console.log(`Glimmer Server running on port ${port}`);
});
