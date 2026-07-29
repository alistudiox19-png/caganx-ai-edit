module.exports = (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  const job_id = Math.random().toString(36).substring(2, 10);
  let action = "basic";
  if (req.body && req.body.action) action = req.body.action;

  return res.status(200).json({
    status: "success",
    job_id: job_id,
    action: action,
    message: "✨ " + action + " Özelliği Başarıyla Tamamlandı!"
  });
};
