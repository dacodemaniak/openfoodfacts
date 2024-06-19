db = db.getSiblingDB('uptake')

db.createUser({
    user: 'uptake_admin',
    pwd: 'admin',
    roles: [
        {
            role: 'dbOwner',
            db: 'uptake'
        }
    ],
    mechanisms: ['SCRAM-SHA-256']
})