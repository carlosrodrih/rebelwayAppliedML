# Week 2 Assignment: Fashion Predictor HDA

![HDA Demo](hda_demo.png)

This project consists of a **Houdini Digital Asset (HDA)** that can load pre-trained neural network models and allows the user to **draw a mask on a grid**, generating a texture that the model uses to **predict which Fashion MNIST item** has been drawn.

Additionally, within the **Google Colab notebook** included in the repository, you will find all the code related to **training the neural network**, as well as the **pre-trained models** used by the HDA.

---

## 🧩 HDA Functionality

The HDA has three main controls:

### **1. File Input — Trained Model**
Allows selecting a `.pth` file corresponding to a pre-trained neural network model.  
The HDA loads this model using the `NNUtils` module.

### **2. Toggle — Save Drawing Texture**
Enables or disables saving the texture generated from the drawing on the grid.  
When enabled, the HDA saves the texture to disk for visual reference or debugging.

### **3. Button — Generate Prediction**
Executes the inference process:  
- Converts the drawn mask into a texture.  
- Sends it to the prediction module.  
- Returns the predicted class name (e.g., *Sneaker*, *Pullover*, *Coat*, etc.).  
- Dynamically updates the **Font** node within the HDA to display the result.

---

## 🧠 Code Structure

### **`nn_utils` Module — `NNUtils` Class**
This module handles:

- Loading the neural network model from the provided path.
- Preparing the image (28×28, grayscale).
- Running inference.
- Returning the predicted class name using Fashion MNIST’s `class_names`.

---

### **`cd_utils` Module — Cd Attribute Management**
This module is responsible for:

- Extracting the **Cd** attribute from the grid where the user draws.  
- Converting it into a valid texture tensor.  
- Preparing it as input for the neural network.

---

### **HDA Internal Script**
The HDA script performs the following tasks:

- Calls `cd_utils` to transform the drawing into a PyTorch-compatible input.
- Calls `NNUtils.predict()` to obtain the model prediction.
- Updates the **Font** node text with the predicted class.
- Optionally saves the generated texture if the toggle is enabled.

---

## 📁 Additional Repository Content

In the **Colab** directory, you will find:

- Full training code.
- Fashion MNIST preprocessing.
- Neural network architecture.
- Pre-trained models ready to be loaded by the HDA.

This setup allows a complete workflow:  
**Train in Colab → Export Model → Predict in Houdini.**

---
