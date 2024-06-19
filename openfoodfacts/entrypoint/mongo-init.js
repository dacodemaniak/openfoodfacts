db = db.getSiblingDB('off')

db.createUser({
    user: 'off_admin',
    pwd: 'admin',
    roles: [
        {
            role: 'dbOwner',
            db: 'off'
        }
    ],
    mechanisms: ['SCRAM-SHA-256']
})