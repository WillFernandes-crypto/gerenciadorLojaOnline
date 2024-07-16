-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
-- José Wilson Fernandes da Silva Júnior
-- Host: localhost
-- Tempo de geração: 17/04/2024 às 15:57
-- Versão do servidor: 10.4.28-MariaDB
-- Versão do PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `LojaOnlinev2`
--
CREATE DATABASE IF NOT EXISTS `LojaOnlinev2` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `LojaOnlinev2`;

-- --------------------------------------------------------

--
-- Estrutura para tabela `Categoria`
--

DROP TABLE IF EXISTS `Categoria`;
CREATE TABLE `Categoria` (
  `idCategoria` int(11) NOT NULL,
  `nomeCategoria` varchar(100) NOT NULL,
  `infoCategoria` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONAMENTOS PARA TABELAS `Categoria`:
--

--
-- Despejando dados para a tabela `Categoria`
--

INSERT INTO `Categoria` (`idCategoria`, `nomeCategoria`, `infoCategoria`) VALUES
(1, 'Eletrônicos', 'Produtos eletrônicos, como televisões, tablets e celulares.');

-- --------------------------------------------------------

--
-- Estrutura para tabela `Cliente`
--

DROP TABLE IF EXISTS `Cliente`;
CREATE TABLE `Cliente` (
  `idCliente` int(11) NOT NULL,
  `endEntrega` varchar(255) NOT NULL,
  `tipoUsuario` enum('CLI') NOT NULL
) ;

--
-- RELACIONAMENTOS PARA TABELAS `Cliente`:
--   `idCliente`
--       `Usuario` -> `idUsuario`
--

--
-- Despejando dados para a tabela `Cliente`
--

INSERT INTO `Cliente` (`idCliente`, `endEntrega`, `tipoUsuario`) VALUES
(1, 'gsrdbdrgsr', 'CLI');

-- --------------------------------------------------------

--
-- Estrutura para tabela `Entrega`
--

DROP TABLE IF EXISTS `Entrega`;
CREATE TABLE `Entrega` (
  `idEntrega` int(11) NOT NULL,
  `idNotaFiscal` int(11) DEFAULT NULL,
  `dataEntregaPrevista` date DEFAULT NULL,
  `dataEntregaReal` date DEFAULT NULL,
  `statusEntrega` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONAMENTOS PARA TABELAS `Entrega`:
--   `idNotaFiscal`
--       `NotaFiscal` -> `idNotaFiscal`
--

--
-- Despejando dados para a tabela `Entrega`
--

INSERT INTO `Entrega` (`idEntrega`, `idNotaFiscal`, `dataEntregaPrevista`, `dataEntregaReal`, `statusEntrega`) VALUES
(1, 1, '2024-08-09', '2024-04-17', 'RECEBIDO');

-- --------------------------------------------------------

--
-- Estrutura para tabela `Fornecedor`
--

DROP TABLE IF EXISTS `Fornecedor`;
CREATE TABLE `Fornecedor` (
  `idFornecedor` int(11) NOT NULL,
  `cnpj` varchar(18) NOT NULL,
  `tipoUsuario` enum('FOR') NOT NULL
) ;

--
-- RELACIONAMENTOS PARA TABELAS `Fornecedor`:
--   `idFornecedor`
--       `Usuario` -> `idUsuario`
--

--
-- Despejando dados para a tabela `Fornecedor`
--

INSERT INTO `Fornecedor` (`idFornecedor`, `cnpj`, `tipoUsuario`) VALUES
(3, '989899899898998', 'FOR');

-- --------------------------------------------------------

--
-- Estrutura para tabela `NotaFiscal`
--

DROP TABLE IF EXISTS `NotaFiscal`;
CREATE TABLE `NotaFiscal` (
  `idNotaFiscal` int(11) NOT NULL,
  `idPagamento` int(11) DEFAULT NULL,
  `dataEmissao` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONAMENTOS PARA TABELAS `NotaFiscal`:
--   `idPagamento`
--       `Pagamento` -> `idPagamento`
--

--
-- Despejando dados para a tabela `NotaFiscal`
--

INSERT INTO `NotaFiscal` (`idNotaFiscal`, `idPagamento`, `dataEmissao`) VALUES
(1, 2, '2024-04-17');

-- --------------------------------------------------------

--
-- Estrutura para tabela `Pagamento`
--

DROP TABLE IF EXISTS `Pagamento`;
CREATE TABLE `Pagamento` (
  `idPagamento` int(11) NOT NULL,
  `idPedido` int(11) DEFAULT NULL,
  `valorTotal` decimal(10,2) NOT NULL,
  `dataPagamento` date NOT NULL,
  `formaPagamento` enum('debito','credito','boleto','pix') NOT NULL,
  `statusPagamento` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONAMENTOS PARA TABELAS `Pagamento`:
--   `idPedido`
--       `Pedido` -> `idPedido`
--

--
-- Despejando dados para a tabela `Pagamento`
--

INSERT INTO `Pagamento` (`idPagamento`, `idPedido`, `valorTotal`, `dataPagamento`, `formaPagamento`, `statusPagamento`) VALUES
(2, 1, 1250.00, '2024-04-17', 'pix', 'FINALIZADO');

-- --------------------------------------------------------

--
-- Estrutura para tabela `Pedido`
--

DROP TABLE IF EXISTS `Pedido`;
CREATE TABLE `Pedido` (
  `idPedido` int(11) NOT NULL,
  `idCliente` int(11) DEFAULT NULL,
  `dataPedido` date NOT NULL,
  `statusPedido` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONAMENTOS PARA TABELAS `Pedido`:
--   `idCliente`
--       `Cliente` -> `idCliente`
--

--
-- Despejando dados para a tabela `Pedido`
--

INSERT INTO `Pedido` (`idPedido`, `idCliente`, `dataPedido`, `statusPedido`) VALUES
(1, 1, '2024-04-17', 'FINALIZADO');

-- --------------------------------------------------------

--
-- Estrutura para tabela `Produto`
--

DROP TABLE IF EXISTS `Produto`;
CREATE TABLE `Produto` (
  `idProduto` int(11) NOT NULL,
  `idFornecedor` int(11) DEFAULT NULL,
  `idCategoria` int(11) DEFAULT NULL,
  `nomeProduto` varchar(100) NOT NULL,
  `infoProduto` text DEFAULT NULL,
  `valorProduto` decimal(10,2) NOT NULL,
  `qtdEstoque` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONAMENTOS PARA TABELAS `Produto`:
--   `idFornecedor`
--       `Fornecedor` -> `idFornecedor`
--   `idCategoria`
--       `Categoria` -> `idCategoria`
--

--
-- Despejando dados para a tabela `Produto`
--

INSERT INTO `Produto` (`idProduto`, `idFornecedor`, `idCategoria`, `nomeProduto`, `infoProduto`, `valorProduto`, `qtdEstoque`) VALUES
(2, 3, 1, 'Televisão', 'LG SMART', 1250.00, 9);

-- --------------------------------------------------------

--
-- Estrutura para tabela `ProdutosPedidos`
--

DROP TABLE IF EXISTS `ProdutosPedidos`;
CREATE TABLE `ProdutosPedidos` (
  `idPedido` int(11) NOT NULL,
  `idProduto` int(11) NOT NULL,
  `qtdEscolhida` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONAMENTOS PARA TABELAS `ProdutosPedidos`:
--   `idPedido`
--       `Pedido` -> `idPedido`
--   `idProduto`
--       `Produto` -> `idProduto`
--

--
-- Despejando dados para a tabela `ProdutosPedidos`
--

INSERT INTO `ProdutosPedidos` (`idPedido`, `idProduto`, `qtdEscolhida`) VALUES
(1, 2, 1);

-- --------------------------------------------------------

--
-- Estrutura para tabela `Promocao`
--

DROP TABLE IF EXISTS `Promocao`;
CREATE TABLE `Promocao` (
  `idPromocao` int(11) NOT NULL,
  `idProduto` int(11) DEFAULT NULL,
  `infoPromocao` text DEFAULT NULL,
  `desconto` decimal(5,2) NOT NULL,
  `dataInicio` date NOT NULL,
  `dataTermino` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONAMENTOS PARA TABELAS `Promocao`:
--   `idProduto`
--       `Produto` -> `idProduto`
--

--
-- Despejando dados para a tabela `Promocao`
--

INSERT INTO `Promocao` (`idPromocao`, `idProduto`, `infoPromocao`, `desconto`, `dataInicio`, `dataTermino`) VALUES
(2, 2, 'black fraude', 0.50, '2024-04-17', '2024-04-18');

-- --------------------------------------------------------

--
-- Estrutura para tabela `Usuario`
--

DROP TABLE IF EXISTS `Usuario`;
CREATE TABLE `Usuario` (
  `idUsuario` int(11) NOT NULL,
  `tipoUsuario` enum('CLI','FOR') NOT NULL,
  `nome` varchar(100) NOT NULL,
  `cpf` varchar(14) NOT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONAMENTOS PARA TABELAS `Usuario`:
--

--
-- Despejando dados para a tabela `Usuario`
--

INSERT INTO `Usuario` (`idUsuario`, `tipoUsuario`, `nome`, `cpf`, `telefone`, `email`) VALUES
(1, 'CLI', 'Wilson', '681681651', '684651898', 'rgdgdrg@gmail.com'),
(3, 'FOR', 'fornecedor', '54545454545', '5665656565', 'efsfsefsefsf@gmail.com');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `Categoria`
--
ALTER TABLE `Categoria`
  ADD PRIMARY KEY (`idCategoria`);

--
-- Índices de tabela `Cliente`
--
ALTER TABLE `Cliente`
  ADD PRIMARY KEY (`idCliente`);

--
-- Índices de tabela `Entrega`
--
ALTER TABLE `Entrega`
  ADD PRIMARY KEY (`idEntrega`),
  ADD KEY `idNotaFiscal` (`idNotaFiscal`);

--
-- Índices de tabela `Fornecedor`
--
ALTER TABLE `Fornecedor`
  ADD PRIMARY KEY (`idFornecedor`),
  ADD UNIQUE KEY `cnpj` (`cnpj`);

--
-- Índices de tabela `NotaFiscal`
--
ALTER TABLE `NotaFiscal`
  ADD PRIMARY KEY (`idNotaFiscal`),
  ADD KEY `idPagamento` (`idPagamento`);

--
-- Índices de tabela `Pagamento`
--
ALTER TABLE `Pagamento`
  ADD PRIMARY KEY (`idPagamento`),
  ADD KEY `idPedido` (`idPedido`);

--
-- Índices de tabela `Pedido`
--
ALTER TABLE `Pedido`
  ADD PRIMARY KEY (`idPedido`),
  ADD KEY `idCliente` (`idCliente`);

--
-- Índices de tabela `Produto`
--
ALTER TABLE `Produto`
  ADD PRIMARY KEY (`idProduto`),
  ADD KEY `idFornecedor` (`idFornecedor`),
  ADD KEY `idCategoria` (`idCategoria`);

--
-- Índices de tabela `ProdutosPedidos`
--
ALTER TABLE `ProdutosPedidos`
  ADD PRIMARY KEY (`idPedido`,`idProduto`),
  ADD KEY `idProduto` (`idProduto`);

--
-- Índices de tabela `Promocao`
--
ALTER TABLE `Promocao`
  ADD PRIMARY KEY (`idPromocao`),
  ADD KEY `idProduto` (`idProduto`);

--
-- Índices de tabela `Usuario`
--
ALTER TABLE `Usuario`
  ADD PRIMARY KEY (`idUsuario`),
  ADD UNIQUE KEY `cpf` (`cpf`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `Categoria`
--
ALTER TABLE `Categoria`
  MODIFY `idCategoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `Entrega`
--
ALTER TABLE `Entrega`
  MODIFY `idEntrega` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de tabela `NotaFiscal`
--
ALTER TABLE `NotaFiscal`
  MODIFY `idNotaFiscal` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `Pagamento`
--
ALTER TABLE `Pagamento`
  MODIFY `idPagamento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `Pedido`
--
ALTER TABLE `Pedido`
  MODIFY `idPedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `Produto`
--
ALTER TABLE `Produto`
  MODIFY `idProduto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `Promocao`
--
ALTER TABLE `Promocao`
  MODIFY `idPromocao` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `Usuario`
--
ALTER TABLE `Usuario`
  MODIFY `idUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `Cliente`
--
ALTER TABLE `Cliente`
  ADD CONSTRAINT `Cliente_ibfk_1` FOREIGN KEY (`idCliente`) REFERENCES `Usuario` (`idUsuario`);

--
-- Restrições para tabelas `Entrega`
--
ALTER TABLE `Entrega`
  ADD CONSTRAINT `Entrega_ibfk_1` FOREIGN KEY (`idNotaFiscal`) REFERENCES `NotaFiscal` (`idNotaFiscal`);

--
-- Restrições para tabelas `Fornecedor`
--
ALTER TABLE `Fornecedor`
  ADD CONSTRAINT `Fornecedor_ibfk_1` FOREIGN KEY (`idFornecedor`) REFERENCES `Usuario` (`idUsuario`);

--
-- Restrições para tabelas `NotaFiscal`
--
ALTER TABLE `NotaFiscal`
  ADD CONSTRAINT `NotaFiscal_ibfk_1` FOREIGN KEY (`idPagamento`) REFERENCES `Pagamento` (`idPagamento`);

--
-- Restrições para tabelas `Pagamento`
--
ALTER TABLE `Pagamento`
  ADD CONSTRAINT `Pagamento_ibfk_1` FOREIGN KEY (`idPedido`) REFERENCES `Pedido` (`idPedido`);

--
-- Restrições para tabelas `Pedido`
--
ALTER TABLE `Pedido`
  ADD CONSTRAINT `Pedido_ibfk_1` FOREIGN KEY (`idCliente`) REFERENCES `Cliente` (`idCliente`);

--
-- Restrições para tabelas `Produto`
--
ALTER TABLE `Produto`
  ADD CONSTRAINT `Produto_ibfk_1` FOREIGN KEY (`idFornecedor`) REFERENCES `Fornecedor` (`idFornecedor`),
  ADD CONSTRAINT `Produto_ibfk_2` FOREIGN KEY (`idCategoria`) REFERENCES `Categoria` (`idCategoria`);

--
-- Restrições para tabelas `ProdutosPedidos`
--
ALTER TABLE `ProdutosPedidos`
  ADD CONSTRAINT `ProdutosPedidos_ibfk_1` FOREIGN KEY (`idPedido`) REFERENCES `Pedido` (`idPedido`),
  ADD CONSTRAINT `ProdutosPedidos_ibfk_2` FOREIGN KEY (`idProduto`) REFERENCES `Produto` (`idProduto`);

--
-- Restrições para tabelas `Promocao`
--
ALTER TABLE `Promocao`
  ADD CONSTRAINT `Promocao_ibfk_1` FOREIGN KEY (`idProduto`) REFERENCES `Produto` (`idProduto`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
