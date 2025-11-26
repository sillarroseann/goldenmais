# Login Credentials Reference

## 🔐 Default Accounts (Preserved After Deployment)

These accounts are created during the first deployment and **NEVER DELETED** on subsequent deployments.

### Admin Account
```
Username: admin
Password: admin123
Email: admin@goldenmais.com
Role: Administrator (Full Access)
```
**Access:** `https://goldenmais.onrender.com/admin/login/`

### Customer Account
```
Username: customer
Password: customer123
Email: customer@goldenmais.com
Role: Customer (Shopping Access)
```
**Access:** `https://goldenmais.onrender.com/login/`

---

## 📝 Important Notes

1. **First Deployment**: Accounts are created automatically
2. **Second Deployment**: Same accounts exist and work
3. **Third+ Deployments**: Accounts continue to work
4. **Data Persistence**: All user data, orders, products remain intact

---

## ✅ Testing Login After Deployment

1. Wait for Render deployment to complete (check Render dashboard)
2. Visit: `https://goldenmais.onrender.com/login/`
3. Enter credentials:
   - Username: `customer`
   - Password: `customer123`
4. Should successfully log in
5. All previous data should be visible

---

## 🆕 Creating Additional Accounts

Users can create new accounts through the signup page:
- **URL**: `https://goldenmais.onrender.com/signup/`
- These accounts are also preserved across deployments

---

## 🔄 Deployment Cycle

| Deployment | Admin Account | Customer Account | User Data |
|-----------|---------------|------------------|-----------|
| 1st | ✅ Created | ✅ Created | ✅ Preserved |
| 2nd | ✅ Exists | ✅ Exists | ✅ Preserved |
| 3rd | ✅ Exists | ✅ Exists | ✅ Preserved |
| 4th+ | ✅ Exists | ✅ Exists | ✅ Preserved |

---

## 🛡️ Why Data is Safe

- **Database**: Managed by Render PostgreSQL (separate from code)
- **Migrations**: Use `get_or_create()` (never deletes)
- **Configuration**: No destructive commands in deployment
- **Result**: All accounts and data persist forever

**Your data is 100% safe!** ✅
