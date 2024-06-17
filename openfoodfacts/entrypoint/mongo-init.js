db = db.getSiblingDB('openfoodfacts')

db.createUser({
    user: 'off_admin',
    pwd: 'admin',
    roles: [
        {
            role: 'dbOwner',
            db: 'openfoodfacts'
        }
    ],
    mechanisms: ['SCRAM-SHA-256']
})