import { useState } from "react";

function AddStock() {
  const [formData, setFormData] = useState({
    company: "",
    quantity: "",
    buyPrice: "",
  });

  function handleChange(e) {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  }

  function handleSubmit(e) {
    e.preventDefault();

    alert(
      `Stock Added!\n\nCompany: ${formData.company}\nQuantity: ${formData.quantity}\nBuy Price: ₹${formData.buyPrice}`
    );

    setFormData({
      company: "",
      quantity: "",
      buyPrice: "",
    });
  }

  return (
    <div
      style={{
        background: "#ffffff",
        padding: "25px",
        borderRadius: "12px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.08)",
        marginBottom: "30px",
      }}
    >
      <h2 style={{ marginBottom: "20px" }}>
        ➕ Add Stock
      </h2>

      <form onSubmit={handleSubmit}>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
            gap: "20px",
          }}
        >
          <input
            type="text"
            name="company"
            placeholder="Company Name"
            value={formData.company}
            onChange={handleChange}
            required
            style={inputStyle}
          />

          <input
            type="number"
            name="quantity"
            placeholder="Quantity"
            value={formData.quantity}
            onChange={handleChange}
            required
            style={inputStyle}
          />

          <input
            type="number"
            name="buyPrice"
            placeholder="Buy Price"
            value={formData.buyPrice}
            onChange={handleChange}
            required
            style={inputStyle}
          />
        </div>

        <button
          type="submit"
          style={{
            marginTop: "20px",
            background: "#2563eb",
            color: "#fff",
            border: "none",
            padding: "12px 30px",
            borderRadius: "8px",
            cursor: "pointer",
            fontSize: "16px",
            fontWeight: "600",
          }}
        >
          Add Stock
        </button>
      </form>
    </div>
  );
}

const inputStyle = {
  padding: "12px",
  border: "1px solid #d1d5db",
  borderRadius: "8px",
  fontSize: "15px",
};

export default AddStock;