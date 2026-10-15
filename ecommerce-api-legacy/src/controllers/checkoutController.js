const { hashPassword, run } = require('../models/database');
const courseModel = require('../models/courseModel');
const userModel = require('../models/userModel');
const enrollmentModel = require('../models/enrollmentModel');
const paymentModel = require('../models/paymentModel');

const checkoutCache = {};

function maskCard(card) {
  if (!card || card.length < 4) return '****';
  return `${'*'.repeat(Math.max(0, card.length - 4))}${card.slice(-4)}`;
}

function logAndCache(key, data) {
  console.log(`[LOG] Salvando no cache: ${key}`);
  checkoutCache[key] = data;
}

async function checkout(req, res, next) {
  try {
    const u = req.body.usr;
    const e = req.body.eml;
    const p = req.body.pwd;
    const cid = req.body.c_id;
    const cc = req.body.card;

    if (!u || !e || !cid || !cc) {
      return res.status(400).send('Bad Request');
    }

    const course = await courseModel.findActiveById(cid);
    if (!course) {
      return res.status(404).send('Curso não encontrado');
    }

    let user = await userModel.findByEmail(e);

    const processPaymentAndEnroll = async (userId) => {
      console.log(`Processando cartão ${maskCard(cc)} no gateway`);
      const status = cc.startsWith('4') ? 'PAID' : 'DENIED';

      if (status === 'DENIED') {
        return res.status(400).send('Pagamento recusado');
      }

      const enrId = await enrollmentModel.create(userId, cid);
      await paymentModel.create(enrId, course.price, status);
      await run(
        "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))",
        [`Checkout curso ${cid} por ${userId}`]
      );

      logAndCache(`last_checkout_${userId}`, course.title);
      return res.status(200).json({ msg: 'Sucesso', enrollment_id: enrId });
    };

    if (!user) {
      const passHash = hashPassword(p || '123456');
      const userId = await userModel.create(u, e, passHash);
      return processPaymentAndEnroll(userId);
    }

    return processPaymentAndEnroll(user.id);
  } catch (err) {
    next(err);
  }
}

module.exports = { checkout, checkoutCache };
