const enrollmentModel = require('../models/enrollmentModel');
const paymentModel = require('../models/paymentModel');
const userModel = require('../models/userModel');

async function deleteUser(req, res, next) {
  try {
    const id = req.params.id;
    const enrollmentIds = await enrollmentModel.findIdsByUserId(id);

    await paymentModel.deleteByEnrollmentIds(enrollmentIds);
    await enrollmentModel.deleteByUserId(id);
    await userModel.deleteById(id);

    return res.send(
      'Usuário deletado junto com matrículas e pagamentos relacionados.'
    );
  } catch (err) {
    next(err);
  }
}

module.exports = { deleteUser };
