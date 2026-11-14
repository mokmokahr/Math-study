# Linear Algebra

## Study Objectives
- For AI study
- Prepare for exams
- Become familiar with English-language Math texts
- Gain a deeper understanding of the mathematical concepts

Focus on challenging concepts and areas that need deeper understanding.  


Reference: https://linear.axler.net/LADR4e.pdf
gif generator: https://github.com/3b1b/manim

## Orthogonal Projection

# vector-to-vectior Orthogonal Projection


```math
\mathrm{proj}_{\mathbf u}(\mathbf v)
=\frac{\mathbf v\cdot\mathbf u}{\mathbf u\cdot\mathbf u}\mathbf u
```

The projection of v onto u is a vector parallel to u. Its length is |u · v| / ||u||.


https://github.com/user-attachments/assets/3a130918-fdf0-4f2d-af31-2eae01d3e150

# vector-to-space Orthogonal Projection

But it's only for vector-to-vector. There is orthogonal projection for vector-to-space.  

Let A be a two-dimensional space with an basis v1 and v2.
(v1 and v2 must be a orthonormal basis)  
Now do orthogonal projection for 2-dimensional space A and vector u.  
Follow these steps.  

1. Project u onto v1.
2. Project u onto v2.
3. Add the two projections.

https://github.com/user-attachments/assets/6505c997-c7ab-44eb-87b9-1ec7181efb92


## How to projection with non-orthogonal vectors?
-> Use orthogonal matrix.  


When we should use orthogonal matrix?  
- When two vectors of space A is not orthogonal each other.  
- Deal with so high dimension(hard to compute each)
- No correct answer for Ax = b(Least square problem)  


```math
p = \Big( A (A^T A)^{-1} A^T \Big) u
```


Orthogonal matrix looks like this.
```math
A(A^{T}A)^{-1}A^{T}
```

Lets treat these problems same with above solution.  
1. Project u onto v1.
2. Project u onto v2.
3. Project u onto v3.
4. Project u onto v4.
...  


If each vectors are all orthonormal vector, we can add the projection vectors.

However, if they are not orthnormal, we should adjust the coefficients considering that the vectors may not be orthonormal...

Moreover, there can be a high-dimensional space.

So, it can be represented as Matrix $A$.
```math
A = \begin{bmatrix} \mid & \mid & & \mid \\ \mathbf{v}_1 & \mathbf{v}_2 & \cdots & \mathbf{v}_n \\ \mid & \mid & & \mid \end{bmatrix}
```
The inner products used in the projection steps (1,2,3,4...) can be calculated using $A^T\mathbf{u}$.
```math
A^T \mathbf{u} = \begin{bmatrix} \mathbf{v}_1^T \mathbf{u} \\ \mathbf{v}_2^T \mathbf{u} \\ \vdots \\ \mathbf{v}_n^T \mathbf{u} \end{bmatrix} = \begin{bmatrix} \mathbf{v}_1 \cdot \mathbf{u} \\ \mathbf{v}_2 \cdot \mathbf{u} \\ \vdots \\ \mathbf{v}_n \cdot \mathbf{u} \end{bmatrix}
```

We have calculated the inner products between $\mathbf{u}$ and each basis vector. If the basis vectors are orthonormal, these inner products are exactly the coefficients we need.

However, for a non-orthonormal basis, these inner products are not necessarily the correct coefficients. We need to determine how much of each basis vector contributes to the final projection.

We want to express vector like this exactly:
```math
\mathbf p=c_1\mathbf v_1+\cdots+c_n\mathbf v_n=A\mathbf c
```

How to get vector c?  

Here is the solution.  
Ac is the orthogonal projection vector.  
So, u-Ac will be the error vector.


https://github.com/user-attachments/assets/2024085f-593a-484b-a47c-961965a6a604

As we can see, error vector and orthogonal vector is vertical.  
So these equation would be accepted.  

```math
A^T(\mathbf u-A\mathbf c)=0
```

```math
A^TA\mathbf c=A^T\mathbf u
```

And, if all column vector of $A$ is linear independant, This equation is possible.  
(Because if it is not linear independant, we can't get inverse matrix.)

```math
\mathbf c=(A^TA)^{-1}A^T\mathbf u
```

Previously, we defined vector c as the coefficient vector of linear combination vector

```math
\mathbf p=c_1\mathbf v_1+\cdots+c_n\mathbf v_n=A\mathbf c
```

We can finally get the vector p, which is orthogonal vector, by multiplying matrix $A$ left of the vector p.  
P = cA (inner product vector c with each column vector of $A$)

There is an Orthogonal Projection Vector.   
```math
\mathbf p=A(A^TA)^{-1}A^T\mathbf u
```
