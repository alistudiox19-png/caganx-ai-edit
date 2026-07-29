module.exports = (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }
  const pre_id = Math.random().toString(36).substring(2, 10);
  return res.status(200).json({ status: "ok", pre_id: pre_id });
};
