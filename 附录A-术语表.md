# 附录 A 推理工程术语表

**Activation function（激活函数）**：（大多）可微的非线性函数，如 ReLU，插入在线性层之间，防止多层神经网络退化成单次矩阵乘法（matmul）。

**Active-active（双活）**：一种高可用姿态，多个区域/集群同时主动承载实时流量。任意一个面（plane）发生故障，流量都会无缝地在其余面上继续服务。

**Active-passive（主备）**：一种故障转移姿态，一个“热备”集群或区域保持就绪但空闲。若活动面失效，流量会切换到备用面。

**Ada Lovelace (architecture)（Ada Lovelace 架构）**：NVIDIA 面向图形的 GPU 架构，于 2022 年与 Hopper 同期发布。适合小模型和成本敏感型工作负载，不适合大规模 LLM 推理。

**Agent（智能体）**：采取行动、而非仅提供信息的 AI 应用。智能体工作流通常依赖多次推理调用，往往跨多个模型和模态，并需要访问工具。

**AI-native application（AI 原生应用）**：核心用户体验和价值都依赖生成式模型的产品。推理选择是应用层约束的下游结果：模态、延迟预算、单位经济性和使用模式。

**Ampere (architecture)（Ampere 架构）**：较旧的 NVIDIA GPU 架构，仍用于遗留或小规模部署。Hopper 和 Blackwell 架构在原始速度和规模化成本上通常都优于 Ampere。

**Application Programming Interface (API)（应用程序编程接口）**：用于发送请求、接收响应的结构化接口。推理引擎对外暴露 API，供向模型发起查询。

**Arithmetic intensity（算术强度）**：给定算法中每移动一个字节所执行的运算次数。将算术强度与 GPU 的 ops:byte 比值相比较，可判断某个 kernel 是受限于计算还是受限于内存。

**Attention（注意力）**：transformer 的核心机制，通过 Q/K/V 投影和 softmax 将一个 token 与先前的 token 关联起来。由于其计算和内存需求，注意力是优化的主要目标。

**Automatic Speech Recognition (ASR)（自动语音识别）**：音频输入、文本输出的转写模型（如 Whisper）。decoder 工作主导运行时间，并受益于 LLM 风格的优化和 in-flight batching。

**Autoregressive token generation（自回归 token 生成）**：迭代式的 token 生成，其中每个 token 都依赖此前的每一个 token。自回归 token 生成分为两个阶段：处理输入 token 的 prefill 阶段，以及生成输出 token 的 decode 阶段。

**Autoscaling（自动扩缩容）**：基于流量或利用率，自动增加或减少某个模型的服务副本数量。自动扩缩容让容量与需求相匹配，维持延迟 SLA 并尽量减少浪费的开支。

**Autoscaling window（扩缩容窗口）**：用于决定扩容/缩容动作的滚动时间窗口。更长的窗口使副本数保持稳定；更短的窗口能更快响应突发流量。

**B200**：NVIDIA 基于 Blackwell 的数据中心 GPU，拥有 192 GB VRAM、8 TB/s 内存带宽和 5 petaFLOPS 的 FP8 计算能力。

**B300**：NVIDIA 基于 Blackwell 的数据中心 GPU，拥有 288 GB VRAM、8 TB/s 内存带宽和 5 petaFLOPS 的 FP8 计算能力。

**Bandwidth（带宽）**：每秒可流经内存（如 VRAM）或互连（如 NVLink）的数据量。

**Baselines（基线）**：在施加优化之前，对性能和质量进行的初步、细致记录的测量。基线使收益或回退能够被清晰地归因。

**Basic Linear Algebra Subprograms (BLAS)（基础线性代数子程序）**：线性代数基本运算的标准接口。

**Batch（批）**：同时处理多个输入，在 LLM 推理中很常见。

**Batch sizing（批大小设定）**：推理引擎中延迟与吞吐量的一个核心权衡杠杆。更大的批能提升总吞吐量，但会恶化单用户延迟。

**Benchmark (intelligence)（智能基准）**：衡量模型正确回答问题或采取恰当行动（如 MMLU）能力的测试。

**Benchmark (performance)（性能基准）**：在定义好的工作负载下，衡量推理服务延迟和吞吐量的测试。

**BF16**：一种 16 位浮点格式，指数范围比 FP16 更大，可用于训练，有时也用于推理。更高的动态范围有助于保留离群值。

**Bin packing (multi-cloud)（装箱，多云）**：将跨云、跨区域、跨集群的异构 GPU 池当作单一可调度资源来处理的实践，由多云容量管理基础设施实现。

**Blackwell (architecture)（Blackwell 架构）**：NVIDIA 于 2024 年末推出的 GPU 代际，支持 FP4、微缩放格式（MXFP8、MXFP4、NVFP4）以及高内存带宽。

**Blue-green deployment（蓝绿部署）**：两套并行的生产环境（“蓝”与“绿”）；在两者之间切换流量，以实现零停机部署和快速回滚。

**Cache-aware routing（缓存感知路由）**：将请求导向已经持有匹配前缀或所需 LoRA 的副本。更高的缓存命中率带来更低的 TTFT。

**Canary deployment（金丝雀部署）**：一种新的生产部署，起初只将一小部分实时流量接入新部署，以验证稳定性和性能。随着时间推移，新部署逐步吸收全部生产流量。

**Causal language model (CLM)（因果语言模型）**：仅含 decoder 的 transformer，根据先前的上下文预测下一个 token。本书中所有生成式 LLM 都是 CLM。

**Central Processing Unit (CPU)（中央处理器）**：一种通用处理器，针对顺序工作负载而优化。CPU 用于编排、调度、网络和预处理，但很少直接承担生成式 AI 推理。

**Chat template（对话模板）**：对消息进行模型特定的格式化与序列化（角色、分隔符、序列起始/结束 token）。

**Chunked prefill（分块 prefill）**：将长输入切分成块，让 prefill 与 decode 或其他工作重叠，防止单个长序列独占资源。

**Classifier-free guidance（无分类器引导）**：在图像生成的每一步去噪中，平衡无条件去噪与提示条件去噪。较低的引导增强创造性；较高的引导强化对提示的遵循。

**CLIP (text encoder)（CLIP，文本编码器）**：早期图像管线（如 SDXL）中使用的文本/图像编码器。现代系统常将其替换为完整 LLM，以获得更强的提示理解能力。

**Closed model（封闭模型）**：权重不可获取的专有模型，如 GPT-5、Claude Sonnet 或 Google Gemini。

**Cold start（冷启动）**：副本从零扩容到首次成功响应所需的时间（步骤包括 GPU 供给、容器启动、模型加载、推理引擎编译）。

**ComfyUI**：用于组装图像管线（基础模型、refiner、LoRA、ControlNet）的工作流工具。鼓励模块化、可替换的组件。

**Compute-bound（计算受限）**：受可用 FLOPS 限制、而非受内存带宽限制的算法。LLM prefill 和图像/视频生成通常是计算受限的。

**Context Parallelism (CP)（上下文并行）**：跨 GPU 复制权重，并切分注意力上下文。对于注意力在庞大潜在空间中运作的视频模型至关重要。

**Context window（上下文窗口）**：模型在单个请求中跨越输入、推理和输出所能处理的最大 token 数。

**Continuous batching (in-flight)（连续批处理，in-flight）**：以 token 为粒度交错处理请求，使 GPU 槽位始终被利用。最大程度减少批处理带来的单用户延迟损失。

**Control plane (multi-cloud)（控制面，多云）**：用于部署模型和分配资源的全局编排器。

**Core (CUDA)（CUDA 核心）**：一种通用算术单元，执行范围广泛的标量和逐元素运算。

**Core (Tensor)（Tensor 核心）**：一种专用硬件单元，针对混合精度矩阵乘加（MMA）运算而优化。Tensor 核心是推理中最重要的一类计算单元。

**Cross-attention（交叉注意力）**：以一个序列作为条件，作用于另一个序列的 K/V 之上（例如，用文本条件来引导图像）。在 multimodal 和去噪管线中很常见。

**cuBLAS**：CUDA 的 BLAS 实现，提供高质量的 GEMM 及相关原语。

**CUDA**：NVIDIA 用于 GPU kernel、图（graph）、内存和执行的编程模型与平台。

**CUDA driver（CUDA 驱动）**：应用程序与 GPU 硬件之间用于管理内存和执行的底层接口。

**CUDA graph（CUDA 图）**：由 kernel 和其他 GPU 操作构成的有向无环图（DAG），用于优化重复性的工作流。

**CUDA kernel（CUDA kernel）**：在 GPU 上执行并行代码的用户自定义函数。

**CUDA runtime（CUDA 运行时）**：面向开发者的 API，用于启动 kernel 和管理内存。

**cuDNN**：用于在 CUDA 中构建深度神经网络的库。

**CuTe**：一个领域特定的 C++ 模板库，对分块张量运算进行抽象，帮助开发者组合出精度感知、硬件优化的 GEMM 与融合 kernel。

**CUTLASS**：一个 CUDA C++ 模板库，提供用于编写高性能、架构调优的 GEMM 及相关 kernel 的构建块。

**Data sovereignty（数据主权）**：对模型输入和输出在地理上处理、存储位置的法定限制。

**Decode（decode 阶段）**：LLM 推理中受内存限制的阶段，自回归生成循环在此阶段每次前向传播输出一个 token。

**DeepGEMM**：由 DeepSeek AI 团队打造的一个简洁高效的 GEMM kernel 库，在 FP8 下表现强劲。

**Denoising model（去噪模型）**：扩散管线的核心，迭代地将潜在噪声精炼为图像或视频。

**Diarization（说话人分离）**：按说话人对音频进行分段（“谁在何时说话”），在 ASR 管线中常与 VAD 配合使用。

**Diffusers (library)（Diffusers 库）**：图像和视频生成管线的参考实现。

**Disaggregation（分离）**：将 prefill 与 decode 拆开到各自独立运行、独立扩缩容、使用不同硬件资源的引擎上。

**Distillation（蒸馏）**：训练一个较小的学生模型去模仿一个较大的教师模型，基于概率分布而非仅基于输出，从而以更少的参数保留模型行为。

**Docker**：一种容器化技术，用于为推理服务及其依赖构建标准化打包。

**Dockerfile**：一种人类可读的文件，包含规范明确、机器可解释的指令，用于创建镜像。

**Dynamic batching（动态批处理）**：当批满或短暂计时器到期（以先到者为准）时，启动一次批处理。平衡延迟稳定性与利用率；已被连续批处理（continuous batching）取代。

**Dynamic range (quantization)（动态范围，量化）**：某种数值格式所能表示的绝对值范围。得益于指数-尾数结构，浮点数的动态范围在同字节数下高于整数。

**EAGLE (speculation)（EAGLE，投机）**：一种小型、专门构建的草稿模型，经训练可消费隐藏状态并提议多个 token，从而在投机解码中获得高接受率。

**Elo (quality meta-metric)（Elo，质量元指标）**：一种两两对决胜负的风格化评分，用于比较模型质量。在智能基准之外，提供有用的方向性信号。

**Embedding model（嵌入模型）**：将文本或图像输入编码为固定维度的向量，用于语义相似度，应用于 RAG 和智能体记忆。现代变体常使用 LLM 主干和 Matryoshka 表示。

**Encoder（编码器）**：将原始输入转换为内部表示（如 Whisper 中的音频特征）的网络。在 encoder-decoder 模型中与 decoder 配对使用。

**Evals（评测）**：复现模型真实世界用例的任务特定测试，用于对模型进行产品特定的智能测试。

**Expert Parallelism (EP)（专家并行）**：将 MoE 的专家分散到多块 GPU 上；每块 GPU 承载多个完整专家。以较低的 GPU 间通信开销提升总吞吐量。

**Few-step image generation（少步图像生成）**：能在八步或更少步骤内生成可用图像的模型。速度快 80%~90%，但有明显的质量取舍；对实时应用来说是有力的选择。

**Feynman (architecture)（Feynman 架构）**：Rubin 之后的一个未来 NVIDIA 代际。细节有限；预计将继续强调低精度和内存带宽。

**Fine-tuning（微调）**：将预训练基础模型适配到某个领域，通常可使小得多的模型也满足质量需求。

**FlashAttention**：一系列经过优化的注意力 kernel，可最小化内存传输。FlashAttention 3 面向 Hopper 编写，FlashAttention 4 面向 Blackwell。

**Floating-point data formats（浮点数据格式）**：推理中使用的 FP16、FP8 和 FP4 等精度，具有较高的动态范围和指数-尾数结构。

**FLOPS**：每秒浮点运算次数，通常以 Tensor 核心为衡量。

**Foundation model（基础模型）**：在海量广泛数据上训练的模型，作为多个下游任务的基座。基础模型（如 GPT、Claude、Llama）通常经微调，或直接通过提示使用。

**Function calling（函数调用）**：又称工具调用（tool calling）或工具使用（tool use），即给模型提供一组可用函数及提示，返回一个结构化输出，其中同时包含所选函数及这些函数的参数。

**GB200**：一款 NVIDIA 超级芯片，通过高带宽 NVLink 芯片间互连，将一颗 Grace CPU 与一块 B200 GPU 配对。GB200 用于机架级 NVLink 系统（如 NVL72），对于受益于 NVLink-C2C 的 KV cache 卸载、LoRA 交换及其他技术很有用。

**General matrix-matrix multiplication (GEMM)（通用矩阵乘法）**：BLAS 中的一种算法，也是推理的关键操作。

**Generative AI（生成式 AI）**：一类模型，与预测式 ML 模型相反，通过学习训练数据的底层模式，跨模态（文本、图像、音频、视频、代码）创建新内容。

**Generative Pretrained Transformer (GPT)（生成式预训练 Transformer）**：由 OpenAI 创建的、用于文本生成的一族大语言模型。

**GH200**：一款 NVIDIA 超级芯片，通过高带宽 NVLink 芯片间互连，将一颗 Grace CPU 与一块 H200 GPU 配对。GH200 用于机架级 NVLink 系统（如 NVL72），对于受益于 NVLink-C2C 的 KV cache 卸载、LoRA 交换及其他技术很有用。

**Goodhart's Law（古德哈特定律）**：“当一项度量成为目标时，它就不再是一个好的度量。”

**GPU node（GPU 节点）**：一种标准机箱，内含 8 块经 NVLink 和 NVSwitch 互连的 GPU。

**Grace CPU**：ARM 架构的 NVIDIA CPU，在 CPU 与 GPU 之间具有高带宽的芯片间互连。与 Hopper 和 Blackwell GPU 配合使用。

**Graphics Processing Unit (GPU)（图形处理器）**：一种高度并行的处理器，最初为图形渲染而设计，如今广泛用于生成式 AI 模型的训练和推理。

**gRPC**：结构化的、以 schema 为先的双向流式协议。

**Head (attention)（注意力头）**：一层内一次独立的注意力计算。

**High-Bandwidth Memory (HBM)（高带宽内存）**：数据中心 GPU 上用作 VRAM 的内存。近期代际包括 HBM3、HBM3e 和 HBM4。

**Hopper (architecture)（Hopper 架构）**：NVIDIA 2022 年的 GPU 代际，支持 FP8 和异步编程特性。

**Hyperscaler（超大规模云厂商）**：泛指类云服务提供商，如 AWS 和 GCP。

**Image generation pipeline（图像生成管线）**：图像生成的基础模型是由多个模型组成的管线：一个文本编码器、一个迭代去噪器和一个 VAE。

**Inference（推理）**：在生产环境中服务 AI 模型。

**Inference engine（推理引擎）**：高性能运行时（vLLM、SGLang、TensorRT-LLM），支持批处理、缓存、量化和投机等优化技术。

**InfiniBand**：用于跨多节点扩展推理和训练的网络节点间互连。虽然 InfiniBand 的带宽高于以太网等替代方案，但它显著低于 NVLink。

**Input sequence（输入序列）**：作为请求一部分提供给模型的 token，在推理的 prefill 阶段被处理。

**Input Sequence Length (ISL)（输入序列长度）**：给定请求中输入序列的 token 数。

**Instance (cloud)（实例，云）**：所供给的虚拟机，包含 GPU、CPU 和 RAM 资源、存储、网络与互连。

**Integer data formats（整数数据格式）**：动态范围有限的数值格式，如 INT8 和 INT4。

**Inter-token latency (ITL)（token 间延迟）**：decode 阶段生成 token 之间的时间。可换算为感知 TPS（例如，2 毫秒 ITL 等于 500 TPS）。

**In-flight batching（in-flight 批处理）**：参见连续批处理（continuous batching）。以 token 为粒度交错处理，实现高利用率并保持延迟稳定。

**Iterative denoising (diffusion)（迭代去噪，扩散）**：从噪声出发，在潜在空间中逐步精炼为图像或视频。

**Jitter traffic (bench)（抖动流量，基准）**：为到达时间和序列形态增加随机性，以更贴近真实流量，而非均匀或突发式的合成负载。

**Kernel fusion（kernel 融合）**：将两个或多个 kernel 取出并重新实现为一个处理这两项操作的单一 kernel，避免经由内存的不必要往返。

**KV cache**：为每个 token 存储的 K/V 张量，以避免重新计算注意力，将注意力计算从二次时间复杂度转化为线性时间复杂度。

**L0/L1/L2 caches (GPU)（L0/L1/L2 缓存，GPU）**：片上缓存内存层级，分别对应指令缓存、共享内存和全局缓存。

**Large Language Model (LLM)（大语言模型）**：一类生成式 AI 模型，接收文本提示并返回一段新的文本序列。许多著名的生成式 AI 模型家族，包括 GPT、Claude、Llama 和 DeepSeek，都是 LLM。

**Latency percentiles（延迟分位数）**：以分位数为基准（P50/P90/P95/P99）测量延迟，以同时感知平均水平与最差情况的用户体验。

**Latent consistency（潜在一致性）**：一种少步策略，能直接预测目标潜在表示，也可能重复进行精炼。速度极快；保真度低于完整扩散。

**Latent space (images/videos)（潜在空间，图像/视频）**：去噪所发生的低维表示空间（例如 128×128）。

**LLM**：大语言模型（如 GPT-5、Llama、DeepSeek）。

**Load testing（负载测试）**：发送持续的高流量，以探查吞吐量上限、排队行为和自动扩缩容能力。

**Local (edge) inference（本地/边缘推理）**：在手机和计算机等终端用户设备上运行推理。

**Logit biasing（logit 偏置）**：对 token 概率进行微调或约束，以引导结构化输出（如 JSON/工具调用）。在采样之前的 post-logits 阶段施加。

**Logits**：非归一化概率组成的向量，模型词表中每个 token 对应一个，在 decode 阶段每次前向传播时生成。

**Lookahead decoding（前瞻解码）**：在推理过程中构造 n-gram，从而无需独立模型即可进行草稿 token 预测。

**LoRA**：低秩适配（low-rank adaptation），一种轻量级微调方法，对模型产生小幅改动。推理服务常常需要针对单个基础模型在数千个 LoRA 之间切换。

**Machine learning (ML)（机器学习）**：针对分类和趋势预测等任务的预测式建模，与创建新颖输出的生成式 AI 相对。

**Matmul（矩阵乘法）**：矩阵相乘。

**Matryoshka representations (embeddings)（Matryoshka 表示，嵌入）**：允许可变维度的嵌套向量方案，其中向量的靠前部分编码更多的语义含义。可在向量大小和嵌入质量之间取舍。

**Medusa (speculation)（Medusa，投机）**：通过微调添加额外的 decoder 头，以在每个遍次中生成多个草稿 token。

**Microscaling formats（微缩放格式）**：MXFP8、MXFP4 和 NVFP4 等浮点数据格式，使用带小分块缩放因子的按块量化（例如每 32 个元素）来提高精度。

**Mixture of Experts (MoE)（混合专家）**：一种模型架构，其线性层的权重被分离为稀疏的专家。路由器为每次前向传播激活一个专家子集。

**Model parallelism (overview)（模型并行，概述）**：通过张量并行、专家并行或流水线并行将工作拆分到多块 GPU 上。并行策略取决于模型规模、拓扑结构，以及延迟与吞吐目标之间的权衡。

**Multi-cloud capacity management（多云容量管理）**：在多个提供商和区域之间放置负载的全局调度器。

**Multi-Instance GPU (MIG)（多实例 GPU）**：Ampere、Hopper、Blackwell 和 Rubin 等较大 GPU 上的一项能力，可将 GPU 切分为至多八个内存切片和七个计算切片。

**Multi-node inference（多节点推理）**：使用 InfiniBand 跨两个或更多节点扩展，当单个由八块 GPU 组成的节点没有足够 VRAM 来容纳权重、激活值和 KV cache 时使用。需要恰当的并行策略，可选 PP 或 EP，因为跨 InfiniBand 使用 TP 会产生过多的全对全（all-to-all）通信。

**Neocloud（新云）**：专注于 GPU 的专门化云服务提供商，如 CoreWeave 和 Nebius。

**Neural audio codec（神经音频编解码器）**：一种学习得到的编码器，将音频压缩为 token，并配有一个配对的 decoder，将 token 转回音频。

**NIM**：由 NVIDIA 创建的、面向特定模型的预打包容器化微服务。

**Node（节点）**：以 NVLink/NVSwitch 相连的物理 8 GPU 基本单元。多节点则在节点之间加入 InfiniBand。

**NVFP4**：NVIDIA 的 4 位浮点微缩放数值格式，具有双缩放因子，以及大小为 16 的按块量化。

**NVIDIA Dynamo**：一个开源的分布式服务托管平台，用于 KV 复用、分离以及多 GPU/多节点编排。

**NVL72**：一种机架级 Blackwell 系统，互连 72 块 GPU 和 36 颗 CPU。专为以极端吞吐量服务超大型模型而构建。

**NVLink**：GPU 之间一对一的通信层，在 Blackwell 上高达 1800 GB/s，在 Hopper 上为 900 GB/s。

**NVSwitch**：位于 NVLink 之上的一层全对全通信层，用于协调节点内所有 GPU 之间的通信。

**N-gram speculation（n-gram 投机）**：利用 prefill 中观测到的 n-gram，在 decode 期间提议较长的草稿序列。对代码补全极其有效。

**Offline inference（离线推理）**：对大批量作业进行异步批处理，针对吞吐量和成本而非单请求延迟进行优化。

**Omni-modal（全模态）**：接受多种模态输入（文本、图像、视频、音频）并产生多种模态输出的模型。

**Online inference（在线推理）**：对请求进行实时服务，针对严格的延迟预算进行优化。

**ONNX**：一种模型中间表示与运行时。

**Open model（开放模型）**：权重可自由获取的模型，如 Llama、DeepSeek 或 Whisper。

**Ops:byte ratio (GPU)（ops:byte 比值，GPU）**：在给定精度下，GPU 每字节内存带宽对应的峰值运算次数。与算术强度相比较，以诊断瓶颈所在。

**Output sequence（输出序列）**：模型在推理的 decode 阶段生成的 token。

**Output Sequence Length (OSL)（输出序列长度）**：对于给定请求，模型所生成的输出序列中的 token 数。

**Out-of-memory error (OOM)（内存不足错误）**：一种常见故障，即 GPU 的 VRAM 不足以加载权重或执行推理。

**PagedAttention**：一种注意力优化，将 KV 块存储在固定大小的分页中，以提升性能，尤其是在长上下文场景下。

**PCIe (GPU form factor)（PCIe，GPU 形态）**：数据中心 GPU 的一种形态因子，使用标准 PCI express 插槽进行连接。同一 GPU 的 PCIe 版本通常基频更低、互连选项更少，不如其 SXM 变体。

**Perceived TPS（感知 TPS）**：单个用户在流式输出期间所观察到的每秒 token 数。这个延迟指标是人们在说 TPS 时通常所指含义的更具体表述。

**Pipeline Parallelism (PP)（流水线并行）**：跨 GPU 将各层切分为多个阶段。对于多节点上的稠密模型可以接受；但 PP 会在流水线中引入气泡（bubble），此时某些 GPU 在等待其他步骤完成时空闲。

**Prefill（prefill 阶段）**：LLM 推理中受计算限制的阶段，在此阶段处理输入序列并构建 KV cache。

**Prefix caching（前缀缓存）**：跨请求复用共享前缀的 KV，以跳过 prefill。大幅改善代码补全、多轮对话和智能体的 TTFT。

**Pretraining（预训练）**：在广泛语料上进行大规模（通常是自监督的）训练，以创建基础模型。

**Prompt（提示）**：给模型的指令；对于扩散模型，还包括一个负向提示以及步数/引导参数。

**PyTorch compile (torch.compile)（PyTorch 编译）**：针对特定 GPU 的图捕获与 kernel 选择/融合。缓存已编译的引擎以缩短冷启动时间。

**PyTorch Profiler（PyTorch 性能分析器）**：一种开发者工具，用于按操作测量 CPU 和 GPU 的时间与内存。

**Quantization (post-training)（量化，训练后）**：降低权重、激活值，以及可能包括 KV cache 的精度，以减少计算和内存带宽需求。

**Quantization-aware training（量化感知训练）**：一种训练技术，其中量化缩放因子被计算、权重被联合优化，使最终模型已针对低精度部署完成校准。

**Queue (request)（队列，请求）**：在自动扩缩容拉起副本期间，暂存多余的流量。

**Real-time factor (RTF)（实时因子）**：衡量 ASR 模型转写音频有多快的指标。转写一小时的音频用六秒，即为 600 的 RTF。

**Retrieval-augmented generation (RAG)（检索增强生成）**：一种常见的应用模式，为 LLM 获取提示之外的额外上下文。

**Ring attention（环形注意力）**：上下文并行中的一种机制，多个 GPU 以环形传递部分的注意力结果。为超大上下文减少全对全的压强。

**Roofline model（屋顶线模型）**：绘制算术强度与带宽、计算上限的关系图，给出一个可视化的指引，说明应当优化内存还是优化计算。

**Rotary positional embeddings (RoPE)（旋转位置嵌入）**：一种位置编码方案，将位置编码为学习得到的旋转，改善长上下文外推能力，代价是推理期间更高的内存需求。

**Routing (inference)（路由，推理）**：基于负载、KV cache、可用的 LoRA 和序列形态，将请求放置到副本上，以提升速度和利用率。

**Rubin (architecture)（Rubin 架构）**：NVIDIA 的下一代（2026 年）代际，引入 HBM4 和 CPX，面向计算受限的工作负载。

**Sampling (decode)（采样，decode）**：基于生成的 logits 选择输出 token 的过程。常见策略包括贪心（argmax）、基于温度的采样、top-k 和 top-p（核）采样。

**Scale factor (quantization)（缩放因子，量化）**：用于将低精度值映射回其原始数值格式的乘数。

**Scale to zero（缩容至零）**：空闲时关闭所有副本，按需再拉起。要求快速的冷启动和稳健的排队；最适合可预测或开发类工作负载。

**SDXL**：一种具有指导性的、较早的扩散图像管线（基础模型 + refiner + CLIP）。现代系统沿用其结构，但使用更大、更强的组件。

**Service Level Agreement (SLA)（服务级别协议）**：一项来自系统的、关于延迟、吞吐量、正常运行时间或其他性能因素的合同性承诺。

**Service Level Objective (SLO)（服务级别目标）**：为实现或超越给定系统 SLA 而设计的内部目标。

**SGLang**：一款快速的推理引擎，具有灵活的前端/后端，并对 MoE 有强力支持。

**Shadow traffic（影子流量）**：将真实的生产请求镜像到候选部署上。

**SNAC (audio decoder)（SNAC，音频解码器）**：一种高性能的音频解码器路径，常与 TTS token 流配合使用。

**Softmax**：在注意力中将分数转换为概率，并在 decode 中将 logits 归一化为概率分布。

**Sparsity (FLOPS)（稀疏性，FLOPS）**：在具有 2:4 结构化稀疏性的张量中，有 50% 的值为 0，Tensor 核心可以跳过乘以 0 的运算。大多数推理是稠密的，而非稀疏的。

**Special Function Unit (SFU)（特殊功能单元）**：一种专用硬件单元，加速 sin、cos 等特定数学运算，使这类专门化操作从 CUDA 核心上卸载出去。

**Speculative decoding（投机解码）**：一族生成并验证草稿 token 的策略，以在 decode 期间每次前向传播生成多个 token。

**Streaming Multiprocessor (SM)（流式多处理器）**：GPU 的计算单元，包含核心和缓存。

**Structured output（结构化输出）**：遵循特定 schema 的 LLM 输出。通过 logit 偏置将生成约束到给定 schema 来创建，而非通过提示。

**SXM (GPU form factor)（SXM，GPU 形态）**：一种插座式的 GPU 模块，支持更高带宽的连接，并提供比 PCIe 更强的性能。SXM 形态的 GPU 通常基频更高，是推理的标准形态。

**Temperature（温度）**：控制 token 选择的随机性：较低的值（如 0.1）使输出更确定；较高的值（如 1.5）增加多样性。

**Tensor Parallelism (TP)（张量并行）**：在节点内跨 GPU 切分张量运算。单用户延迟最佳；需要频繁的全规约（all-reduce）同步。

**TensorRT**：NVIDIA 的优化运行时，用于高性能推理，支持融合 kernel、量化及其他优化。

**TensorRT-LLM**：由 NVIDIA 构建的一款推理引擎，提供 Python API，以及带融合 kernel、量化和投机解码的 TensorRT 引擎和 PyTorch 后端两条执行路径。

**Thread（线程）**：GPU 上最小的执行单元。Kernel 启动大量线程以实现大规模并行。

**Throughput（吞吐量）**：单位时间内完成的总工作量（如每秒的总 token 数）。

**Time to first byte (TTFB)（首字节时间）**：返回输出的第一个字节之前的用时，是一种延迟指标。

**Time to first token (TTFT)（首 token 时间）**：返回输出的第一个 token 之前的用时，是一种延迟指标。

**Token**：LLM 中文本处理的原子单位。一个 token 是一个代表字符串的整数。对于大多数分词器，英文中大约为 4:3 的 token 与词之比。

**Tokenizer（分词器）**：确定性地将字符串转换为 token 序列，反之亦然。不同模型有不同的分词器，更高效的分词器可改善端到端延迟。

**Tokens per second (TPS)（每秒 token 数）**：参见感知 TPS（perceived TPS）。一种延迟指标，衡量每秒流向终端用户的 token 数。

**Training（训练）**：通过反向传播和优化，从数据中学习模型权重的过程。训练是计算密集型的，通常在大型 GPU 集群上运行，并产出推理中所使用的权重。

**Transformer**：生成式 AI 模型背后的基础架构。

**Transformers (library)（Transformers 库）**：LLM 及其他基于 transformer 模型的参考实现。

**Triton Inference Server（Triton 推理服务器）**：由 NVIDIA 打造的一款生产级服务托管框架，支持多种后端。

**VAE (variational autoencoder)（VAE，变分自编码器）**：在推理中用于从潜在空间解码到像素空间，以生成图像和视频（训练时也用于从像素编码到潜在空间）。

**Vector database（向量数据库）**：用于存储和查询由嵌入模型创建的语义向量的数据库。

**Vector similarity（向量相似度）**：基于余弦相似度之类的等式，检查两个向量彼此有多接近。相似度高的向量编码相似的语义。

**Vera CPU**：ARM 架构的 NVIDIA CPU，在 CPU 与 GPU 之间具有高带宽的芯片间互连。在 Rubin GPU 架构代际中接替 Grace CPU。

**Vision-language model (VLM)（视觉语言模型）**：接受图像和视频外加文本提示，并输出文本。

**vLLM**：一款被广泛采用的推理引擎，具有广泛的模型与硬件支持以及强大的默认配置。

**Vocabulary（词表）**：LLM 用于表示数据的 token 全集，通常超过 100,000 个。

**Voice activity detection (VAD)（语音活动检测）**：一种轻量级模型，将音频流/文件切分为包含语音的块，供 ASR 使用。

**VRAM (device memory)（VRAM，设备内存）**：GPU 上用于权重、KV 和激活值的内存。VRAM 总量决定模型大小上限和 KV 余量；带宽决定 decode TPS。

**WebSocket**：轻量级、双向的流式传输。适合非结构化音频块和实时体验。

**Weights-only quantization（仅权重量化）**：降低线性层模型权重的精度，同时让 KV cache 和注意力等其他模型组件保持较高精度。一种保守的量化方法，质量保留最好，但性能提升最低。

**Workload plane (multi-cloud)（工作负载面，多云）**：一个具有计算资源的独立集群，负责运行推理并处理请求。
